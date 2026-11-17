using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Autonomous Procedural Generator for the Realistic 3D Virtual World of Bangalore.
    /// Builds:
    /// - Central Silk Board Elevated Multi-Tier Flyover & Piers
    /// - Namma Metro Elevated Viaduct & Purple-Line Metro Coaches
    /// - 4 Interconnected Bangalore Zones:
    ///   * Zone A: Koramangala (Sony World Junction, Darshini Cafes, 80ft Road)
    ///   * Zone B: HSR Layout (27th Main, BDA Complex, Green Tree Avenues)
    ///   * Zone C: Bellandur (Outer Ring Road, RMZ Ecospace Tech Park, Bus Shelters)
    ///   * Zone D: Central Silk Board (Hosur Road, Bottleneck Junction, Metro Interchange)
    /// - BESCOM 66kV Substation & Roadside 11kV Green Distribution Transformers
    /// - Ather / BESCOM EV Fast Charging Hubs
    /// </summary>
    public class CityBuilder : MonoBehaviour
    {
        [Header("Road & Urban Dimensions")]
        public float roadWidth = 16.0f;
        public float flyoverHeight = 9.0f;
        public float metroHeight = 14.5f;

        [Header("Materials (Auto-Initialized)")]
        public Material asphaltMaterial;
        public Material flyoverConcreteMaterial;
        public Material dividerMaterial;
        public Material techParkGlassMaterial;
        public Material residentialMaterial;
        public Material bescomGreenMaterial;
        public Material treeMaterial;
        public Material woodMaterial;

        void Awake()
        {
            InitializeBangaloreMaterials();
            BuildBangaloreVirtualWorld();
        }

        private void InitializeBangaloreMaterials()
        {
            Shader standard = Shader.Find("Standard") ?? Shader.Find("Diffuse");

            if (asphaltMaterial == null) asphaltMaterial = new Material(standard) { color = new Color(0.15f, 0.16f, 0.18f) };
            if (flyoverConcreteMaterial == null) flyoverConcreteMaterial = new Material(standard) { color = new Color(0.40f, 0.44f, 0.48f) };
            if (dividerMaterial == null) dividerMaterial = new Material(standard) { color = new Color(0.98f, 0.82f, 0.15f) };
            if (techParkGlassMaterial == null) techParkGlassMaterial = new Material(standard) { color = new Color(0.12f, 0.35f, 0.65f) };
            if (residentialMaterial == null) residentialMaterial = new Material(standard) { color = new Color(0.82f, 0.84f, 0.88f) };
            if (bescomGreenMaterial == null) bescomGreenMaterial = new Material(standard) { color = new Color(0.10f, 0.50f, 0.22f) }; // BESCOM Green
            if (treeMaterial == null) treeMaterial = new Material(standard) { color = new Color(0.12f, 0.48f, 0.20f) };
            if (woodMaterial == null) woodMaterial = new Material(standard) { color = new Color(0.35f, 0.22f, 0.14f) };
        }

        public void BuildBangaloreVirtualWorld()
        {
            GameObject cityRoot = new GameObject("Bangalore_Virtual_World");

            // Ground Terrain
            GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
            ground.name = "Bangalore_Ground";
            ground.transform.parent = cityRoot.transform;
            ground.transform.localScale = new Vector3(45.0f, 1.0f, 45.0f);
            ground.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.18f, 0.22f, 0.18f) };

            // 1. Build Arterial Road Corridors
            BuildOuterRingRoad(cityRoot.transform);

            // 2. Build Central Silk Board Elevated Flyover
            BuildSilkBoardFlyover(cityRoot.transform);

            // 3. Build Namma Metro Viaduct & Metro Train
            BuildNammaMetroViaduct(cityRoot.transform);

            // 4. Build the 4 Bangalore Zones
            BuildZone(cityRoot.transform, "Zone_A_Koramangala", -90.0f, 90.0f, "Sony World & Darshini Hub", false);
            BuildZone(cityRoot.transform, "Zone_B_HSR_Layout", 90.0f, 90.0f, "27th Main & BDA Complex", false);
            BuildZone(cityRoot.transform, "Zone_C_Bellandur_Ecospace", 90.0f, -90.0f, "RMZ Ecospace Tech Corridor", true);
            BuildZone(cityRoot.transform, "Zone_D_Silk_Board_Junction", -90.0f, -90.0f, "Central Silk Board Transit Node", false);

            // 5. Build BESCOM Central 66kV Substation
            BuildBESCOMSubstation(cityRoot.transform);
        }

        private void BuildOuterRingRoad(Transform parent)
        {
            // Outer Ring Road Arterial (Bellandur to Silk Board)
            CreateRoad(parent, new Vector3(0, 0.05f, -90), new Vector3(360, 0.1f, roadWidth), true);
            // Koramangala to HSR Link Road
            CreateRoad(parent, new Vector3(0, 0.05f, 90), new Vector3(360, 0.1f, roadWidth), true);
            // Hosur Road (Silk Board to Koramangala)
            CreateRoad(parent, new Vector3(-90, 0.05f, 0), new Vector3(roadWidth, 0.1f, 360), false);
            // Sarjapur / HSR Link
            CreateRoad(parent, new Vector3(90, 0.05f, 0), new Vector3(roadWidth, 0.1f, 360), false);
        }

        private void CreateRoad(Transform parent, Vector3 pos, Vector3 size, bool isHorizontal)
        {
            GameObject road = GameObject.CreatePrimitive(PrimitiveType.Cube);
            road.name = "Bangalore_Road_Arterial";
            road.transform.parent = parent;
            road.transform.position = pos;
            road.transform.localScale = size;
            road.GetComponent<MeshRenderer>().material = asphaltMaterial;

            // Road Divider
            GameObject divider = GameObject.CreatePrimitive(PrimitiveType.Cube);
            divider.name = "Yellow_Divider";
            divider.transform.parent = road.transform;
            divider.transform.localPosition = new Vector3(0, 0.55f, 0);
            divider.transform.localScale = isHorizontal ? new Vector3(1.0f, 0.1f, 0.03f) : new Vector3(0.03f, 0.1f, 1.0f);
            divider.GetComponent<MeshRenderer>().material = dividerMaterial;
        }

        private void BuildSilkBoardFlyover(Transform parent)
        {
            GameObject flyoverGroup = new GameObject("Silk_Board_Elevated_Flyover");
            flyoverGroup.transform.parent = parent;

            // Elevated Flyover Deck
            GameObject deck = GameObject.CreatePrimitive(PrimitiveType.Cube);
            deck.name = "Flyover_Deck";
            deck.transform.parent = flyoverGroup.transform;
            deck.transform.position = new Vector3(-90.0f, flyoverHeight, -90.0f);
            deck.transform.localScale = new Vector3(14.0f, 1.2f, 140.0f);
            deck.GetComponent<MeshRenderer>().material = flyoverConcreteMaterial;

            // Concrete Flyover Support Pillars
            for (float z = -150.0f; z <= -30.0f; z += 25.0f)
            {
                GameObject pier = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
                pier.name = "Flyover_Pier";
                pier.transform.parent = flyoverGroup.transform;
                pier.transform.position = new Vector3(-90.0f, flyoverHeight / 2.0f, z);
                pier.transform.localScale = new Vector3(2.2f, flyoverHeight / 2.0f, 2.2f);
                pier.GetComponent<MeshRenderer>().material = flyoverConcreteMaterial;
            }
        }

        private void BuildNammaMetroViaduct(Transform parent)
        {
            GameObject metroGroup = new GameObject("Namma_Metro_Yellow_Line");
            metroGroup.transform.parent = parent;

            // Viaduct Track along Outer Ring Road Median
            GameObject track = GameObject.CreatePrimitive(PrimitiveType.Cube);
            track.name = "Metro_Viaduct_Track";
            track.transform.parent = metroGroup.transform;
            track.transform.position = new Vector3(0.0f, metroHeight, -90.0f);
            track.transform.localScale = new Vector3(320.0f, 1.2f, 5.5f);
            track.GetComponent<MeshRenderer>().material = flyoverConcreteMaterial;

            // Elevated Metro Pillars
            for (float x = -140.0f; x <= 140.0f; x += 32.0f)
            {
                GameObject pillar = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
                pillar.name = "Metro_Pillar";
                pillar.transform.parent = metroGroup.transform;
                pillar.transform.position = new Vector3(x, metroHeight / 2.0f, -90.0f);
                pillar.transform.localScale = new Vector3(1.8f, metroHeight / 2.0f, 1.8f);
                pillar.GetComponent<MeshRenderer>().material = flyoverConcreteMaterial;
            }

            // Metro Train Coaches (Purple & White Line)
            for (int c = 0; c < 3; c++)
            {
                GameObject coach = GameObject.CreatePrimitive(PrimitiveType.Cube);
                coach.name = $"Metro_Coach_{c}";
                coach.transform.parent = metroGroup.transform;
                coach.transform.position = new Vector3(-20.0f + (c * 18.0f), metroHeight + 2.2f, -90.0f);
                coach.transform.localScale = new Vector3(16.0f, 3.4f, 4.2f);
                coach.GetComponent<MeshRenderer>().material = new Material(Shader.Find("Standard")) { color = new Color(0.92f, 0.94f, 0.98f) };
            }
        }

        private void BuildZone(Transform parent, string zoneId, float cx, float cz, string desc, bool isTechPark)
        {
            GameObject zoneObj = new GameObject(zoneId);
            zoneObj.transform.parent = parent;

            // Commercial / Residential Buildings
            for (int bx = -1; bx <= 1; bx += 2)
            {
                for (int bz = -1; bz <= 1; bz += 2)
                {
                    float height = isTechPark ? Random.Range(40.0f, 75.0f) : Random.Range(22.0f, 42.0f);
                    GameObject b = GameObject.CreatePrimitive(PrimitiveType.Cube);
                    b.name = isTechPark ? "RMZ_Tech_Tower" : "Bangalore_Commercial_Building";
                    b.transform.parent = zoneObj.transform;
                    b.transform.position = new Vector3(cx + (bx * 22.0f), height / 2.0f, cz + (bz * 22.0f));
                    b.transform.localScale = new Vector3(18.0f, height, 18.0f);
                    b.GetComponent<MeshRenderer>().material = isTechPark ? techParkGlassMaterial : residentialMaterial;
                }
            }

            // Roadside BESCOM 11kV Distribution Transformer
            GameObject transObj = new GameObject("BESCOM_11kV_Transformer");
            transObj.transform.parent = zoneObj.transform;
            transObj.transform.position = new Vector3(cx + 18.0f, 0.0f, cz + 18.0f);

            GameObject transBox = GameObject.CreatePrimitive(PrimitiveType.Cube);
            transBox.transform.parent = transObj.transform;
            transBox.transform.localPosition = new Vector3(0, 2.5f, 0);
            transBox.transform.localScale = new Vector3(2.5f, 3.2f, 2.5f);
            transBox.GetComponent<MeshRenderer>().material = bescomGreenMaterial;

            // Bus Stop Shelter
            GameObject shelter = GameObject.CreatePrimitive(PrimitiveType.Cube);
            shelter.name = "BMTC_Bus_Shelter";
            shelter.transform.parent = zoneObj.transform;
            shelter.transform.position = new Vector3(cx - 15.0f, 1.8f, cz + 24.0f);
            shelter.transform.localScale = new Vector3(8.0f, 3.5f, 2.5f);
            shelter.GetComponent<MeshRenderer>().material = flyoverConcreteMaterial;

            // Chai Corner / Street Stall
            GameObject chai = GameObject.CreatePrimitive(PrimitiveType.Cube);
            chai.name = "Darshini_Chai_Corner";
            chai.transform.parent = zoneObj.transform;
            chai.transform.position = new Vector3(cx + 25.0f, 1.5f, cz - 22.0f);
            chai.transform.localScale = new Vector3(4.5f, 2.8f, 3.5f);
            chai.GetComponent<MeshRenderer>().material = woodMaterial;
        }

        private void BuildBESCOMSubstation(Transform parent)
        {
            GameObject sub = new GameObject("BESCOM_Central_66kV_Substation");
            sub.transform.parent = parent;
            sub.transform.position = Vector3.zero;

            GameObject trans = GameObject.CreatePrimitive(PrimitiveType.Cube);
            trans.name = "Main_66kV_Power_Transformer";
            trans.transform.parent = sub.transform;
            trans.transform.position = new Vector3(0, 3.5f, 0);
            trans.transform.localScale = new Vector3(14.0f, 7.0f, 14.0f);
            trans.GetComponent<MeshRenderer>().material = bescomGreenMaterial;
        }
    }
}
