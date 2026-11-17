using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

namespace CityLink
{
    /// <summary>
    /// Master Orchestration Manager for the 3D Virtual World of Bangalore.
    /// Streams live telemetry from FastAPI backend and instantiates authentic Bangalore transport:
    /// - BMTC Buses (Vajra Blue Volvo & Green City Buses)
    /// - Bengaluru Auto-Rickshaws (Iconic Yellow Top & Green Body)
    /// - Two-Wheelers with Swiggy/Zomato Delivery Boxes
    /// - IT Cabs & Ambulances
    /// - Techies, Students, and Commuters walking on sidewalks
    /// - 16 Traffic Signals & BESCOM 11kV Distribution Feeders
    /// </summary>
    public class CityLinkManager : MonoBehaviour
    {
        [Header("Backend Connection")]
        public string apiBaseUrl = "http://localhost:8000/api";
        public float pollingInterval = 0.1f;

        [Header("Runtime Pools")]
        private Dictionary<string, VehicleController> activeVehicles = new Dictionary<string, VehicleController>();
        private Dictionary<string, PedestrianController> activePedestrians = new Dictionary<string, PedestrianController>();
        private Dictionary<string, TrafficLightController> activeSignals = new Dictionary<string, TrafficLightController>();
        private Dictionary<string, PowerFeederVisualizer> activeFeeders = new Dictionary<string, PowerFeederVisualizer>();

        private Transform vehicleContainer;
        private Transform pedestrianContainer;
        private Transform signalContainer;
        private Transform feederContainer;

        void Start()
        {
            vehicleContainer = new GameObject("Bangalore_Fleet_Pool").transform;
            pedestrianContainer = new GameObject("Bangalore_Pedestrian_Pool").transform;
            signalContainer = new GameObject("Bangalore_Signals_Pool").transform;
            feederContainer = new GameObject("BESCOM_Feeders_Pool").transform;

            StartCoroutine(PollTelemetryRoutine());
        }

        void Update()
        {
            // Scenario triggers
            if (Input.GetKeyDown(KeyCode.F1)) TriggerScenario("NORMAL_CITY");
            if (Input.GetKeyDown(KeyCode.F2)) TriggerScenario("TRAFFIC_CONGESTION");
            if (Input.GetKeyDown(KeyCode.F3)) TriggerScenario("POWER_FAILURE");
            if (Input.GetKeyDown(KeyCode.F4)) TriggerScenario("CYBERATTACK");
            if (Input.GetKeyDown(KeyCode.F5)) TriggerScenario("AUTOMATIC_RECOVERY");
            if (Input.GetKeyDown(KeyCode.R)) ResetSimulation();
        }

        private IEnumerator PollTelemetryRoutine()
        {
            while (true)
            {
                using (UnityWebRequest req = UnityWebRequest.Get($"{apiBaseUrl}/status"))
                {
                    yield return req.SendWebRequest();

                    if (req.result == UnityWebRequest.Result.Success)
                    {
                        ParseAndApplyState(req.downloadHandler.text);
                    }
                }
                yield return new WaitForSeconds(pollingInterval);
            }
        }

        private void ParseAndApplyState(string json)
        {
            try
            {
                SimpleJSONNode root = SimpleJSONNode.Parse(json);
                if (root == null) return;

                // 1. Process Bangalore Fleet
                var vehArray = root["entities"]["vehicles"];
                if (vehArray != null)
                {
                    HashSet<string> seen = new HashSet<string>();
                    for (int i = 0; i < vehArray.Count; i++)
                    {
                        var v = vehArray[i];
                        string vid = v["id"].Value;
                        seen.Add(vid);

                        Vector3 pos = new Vector3(v["x"].AsFloat, v["y"].AsFloat, v["z"].AsFloat);
                        float heading = v["heading"].AsFloat;
                        float speed = v["speed"].AsFloat;
                        bool braking = v["braking"].AsBool;
                        bool queued = v["in_queue"].AsBool;
                        bool isEmergency = v["is_emergency"].AsBool;
                        string vtype = v["type"].Value;

                        if (!activeVehicles.ContainsKey(vid))
                        {
                            GameObject vObj = CreateBangaloreVehicle(vid, vtype);
                            vObj.transform.parent = vehicleContainer;
                            VehicleController ctrl = vObj.GetComponent<VehicleController>();
                            activeVehicles[vid] = ctrl;
                        }

                        activeVehicles[vid].UpdateTelemetry(pos, heading, speed, braking, queued, isEmergency);
                    }

                    List<string> toRemove = new List<string>();
                    foreach (var k in activeVehicles.Keys)
                    {
                        if (!seen.Contains(k)) toRemove.Add(k);
                    }
                    foreach (var k in toRemove)
                    {
                        Destroy(activeVehicles[k].gameObject);
                        activeVehicles.Remove(k);
                    }
                }

                // 2. Process Bangalore Pedestrians (Techies, Commuters)
                var pedArray = root["entities"]["pedestrians"];
                if (pedArray != null)
                {
                    for (int i = 0; i < pedArray.Count; i++)
                    {
                        var p = pedArray[i];
                        string pid = p["id"].Value;
                        Vector3 pos = new Vector3(p["x"].AsFloat, p["y"].AsFloat, p["z"].AsFloat);
                        float heading = p["heading"].AsFloat;
                        string pstate = p["state"].Value;

                        if (!activePedestrians.ContainsKey(pid))
                        {
                            GameObject pObj = CreateBangalorePedestrian(pid);
                            pObj.transform.parent = pedestrianContainer;
                            PedestrianController pCtrl = pObj.GetComponent<PedestrianController>();
                            activePedestrians[pid] = pCtrl;
                        }

                        activePedestrians[pid].UpdateTelemetry(pos, heading, pstate);
                    }
                }

                // 3. Process Signals
                var sigObj = root["traffic"]["signals"];
                if (sigObj != null)
                {
                    foreach (var key in sigObj.Keys)
                    {
                        var s = sigObj[key];
                        string sid = s["signal_id"].Value;
                        string status = s["status"].Value;
                        string light = s["ns_light"].Value;
                        bool pedWalk = s["pedestrian_walk"].AsBool;

                        if (!activeSignals.ContainsKey(sid))
                        {
                            Vector3 pos = new Vector3(s["pos"][0].AsFloat, s["pos"][1].AsFloat, s["pos"][2].AsFloat);
                            GameObject sObj = CreateDefaultSignalPole(pos, sid);
                            sObj.transform.parent = signalContainer;
                            activeSignals[sid] = sObj.GetComponent<TrafficLightController>();
                        }

                        activeSignals[sid].SetState(status, light, pedWalk);
                    }
                }

                // 4. Process BESCOM Feeders
                var feederObj = root["power"]["feeders"];
                if (feederObj != null)
                {
                    foreach (var fid in feederObj.Keys)
                    {
                        var f = feederObj[fid];
                        float load = f["physical_load_mw"].AsFloat;
                        float pct = f["loading_percentage"].AsFloat;
                        string fStatus = f["status"].Value;
                        bool closed = f["breaker_closed"].AsBool;

                        if (!activeFeeders.ContainsKey(fid))
                        {
                            GameObject fObj = new GameObject($"BESCOM_{fid}");
                            fObj.transform.parent = feederContainer;
                            PowerFeederVisualizer pfv = fObj.AddComponent<PowerFeederVisualizer>();
                            pfv.feederId = fid;
                            activeFeeders[fid] = pfv;
                        }

                        activeFeeders[fid].UpdateFeederState(load, pct, fStatus, closed);
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogWarning($"[CityLinkManager] Error: {ex.Message}");
            }
        }

        private GameObject CreateBangaloreVehicle(string vid, string vtype)
        {
            GameObject v = new GameObject($"Veh_{vid}");

            if (vtype == "bmtc_bus")
            {
                // BMTC Bus (Blue AC Vajra or Green Bus)
                GameObject bus = GameObject.CreatePrimitive(PrimitiveType.Cube);
                bus.transform.parent = v.transform;
                bus.transform.localScale = new Vector3(2.6f, 3.2f, 10.8f);
                bus.transform.localPosition = new Vector3(0, 1.6f, 0);
                Color busCol = (UnityEngine.Random.value > 0.5f) ? new Color(0.08f, 0.45f, 0.85f) : new Color(0.12f, 0.65f, 0.30f);
                bus.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = busCol };

                // Destination Board ('500-D SILK BOARD')
                GameObject board = GameObject.CreatePrimitive(PrimitiveType.Cube);
                board.transform.parent = bus.transform;
                board.transform.localPosition = new Vector3(0, 0.42f, 0.51f);
                board.transform.localScale = new Vector3(0.8f, 0.12f, 0.02f);
                board.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = Color.yellow };
            }
            else if (vtype == "auto_rickshaw")
            {
                // Bangalore Auto-Rickshaw (Yellow Top & Green Base)
                GameObject hood = GameObject.CreatePrimitive(PrimitiveType.Cube);
                hood.transform.parent = v.transform;
                hood.transform.localScale = new Vector3(1.4f, 0.8f, 2.6f);
                hood.transform.localPosition = new Vector3(0, 1.5f, 0);
                hood.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.95f, 0.80f, 0.10f) }; // Yellow

                GameObject baseObj = GameObject.CreatePrimitive(PrimitiveType.Cube);
                baseObj.transform.parent = v.transform;
                baseObj.transform.localScale = new Vector3(1.4f, 0.9f, 2.8f);
                baseObj.transform.localPosition = new Vector3(0, 0.65f, 0);
                baseObj.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.10f, 0.55f, 0.22f) }; // Green
            }
            else if (vtype == "delivery_bike")
            {
                // Two-wheeler with Swiggy/Zomato delivery bag
                GameObject bike = GameObject.CreatePrimitive(PrimitiveType.Cube);
                bike.transform.parent = v.transform;
                bike.transform.localScale = new Vector3(0.6f, 1.1f, 1.9f);
                bike.transform.localPosition = new Vector3(0, 0.6f, 0);
                bike.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.2f, 0.2f, 0.2f) };

                GameObject box = GameObject.CreatePrimitive(PrimitiveType.Cube);
                box.transform.parent = v.transform;
                box.transform.localScale = new Vector3(0.7f, 0.7f, 0.7f);
                box.transform.localPosition = new Vector3(0, 1.15f, -0.6f);
                Color boxColor = (UnityEngine.Random.value > 0.5f) ? new Color(0.95f, 0.40f, 0.10f) : new Color(0.85f, 0.15f, 0.15f); // Swiggy Orange or Zomato Red
                box.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = boxColor };
            }
            else if (vtype == "emergency")
            {
                // 108 Ambulance
                GameObject amb = GameObject.CreatePrimitive(PrimitiveType.Cube);
                amb.transform.parent = v.transform;
                amb.transform.localScale = new Vector3(2.2f, 2.4f, 5.5f);
                amb.transform.localPosition = new Vector3(0, 1.2f, 0);
                amb.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = Color.white };

                // Flashing beacon
                GameObject siren = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
                siren.transform.parent = amb.transform;
                siren.transform.localPosition = new Vector3(0, 0.6f, 0.1f);
                siren.transform.localScale = new Vector3(0.25f, 0.2f, 0.25f);
                siren.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = Color.red };
            }
            else
            {
                // Corporate IT Cab / Sedan
                GameObject car = GameObject.CreatePrimitive(PrimitiveType.Cube);
                car.transform.parent = v.transform;
                car.transform.localScale = new Vector3(1.8f, 1.4f, 4.2f);
                car.transform.localPosition = new Vector3(0, 0.7f, 0);
                car.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = (vtype == "it_cab") ? Color.white : new Color(0.25f, 0.50f, 0.85f) };
            }

            VehicleController ctrl = v.AddComponent<VehicleController>();
            ctrl.vehicleId = vid;
            ctrl.vehicleType = vtype;
            ctrl.isEmergency = (vtype == "emergency");
            return v;
        }

        private GameObject CreateBangalorePedestrian(string pid)
        {
            GameObject p = new GameObject($"Ped_{pid}");
            GameObject body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            body.transform.parent = p.transform;
            body.transform.localScale = new Vector3(0.55f, 0.9f, 0.55f);
            body.transform.localPosition = new Vector3(0, 0.9f, 0);
            body.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.2f, 0.6f, 0.9f) };

            // Techie backpack
            GameObject bag = GameObject.CreatePrimitive(PrimitiveType.Cube);
            bag.transform.parent = body.transform;
            bag.transform.localPosition = new Vector3(0, 0.2f, -0.45f);
            bag.transform.localScale = new Vector3(0.6f, 0.7f, 0.35f);
            bag.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.1f, 0.12f, 0.15f) };

            PedestrianController pCtrl = p.AddComponent<PedestrianController>();
            pCtrl.pedestrianId = pid;
            return p;
        }

        private GameObject CreateDefaultSignalPole(Vector3 pos, string sid)
        {
            GameObject poleObj = new GameObject($"Signal_{sid}");
            poleObj.transform.position = pos;

            GameObject pole = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            pole.transform.parent = poleObj.transform;
            pole.transform.localPosition = new Vector3(0, 3.0f, 0);
            pole.transform.localScale = new Vector3(0.25f, 3.0f, 0.25f);

            GameObject head = GameObject.CreatePrimitive(PrimitiveType.Cube);
            head.transform.parent = poleObj.transform;
            head.transform.localPosition = new Vector3(0, 5.5f, 0);
            head.transform.localScale = new Vector3(0.8f, 2.0f, 0.6f);
            head.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = Color.black };

            TrafficLightController tlc = poleObj.AddComponent<TrafficLightController>();
            tlc.signalId = sid;
            return poleObj;
        }

        public void TriggerScenario(string scenarioName)
        {
            StartCoroutine(PostScenarioRoutine(scenarioName));
        }

        private IEnumerator PostScenarioRoutine(string scenarioName)
        {
            using (UnityWebRequest req = UnityWebRequest.PostWwwForm($"{apiBaseUrl}/scenario/{scenarioName}", ""))
            {
                yield return req.SendWebRequest();
            }
        }

        public void ResetSimulation()
        {
            StartCoroutine(PostScenarioRoutine("NORMAL_CITY"));
        }
    }
}
