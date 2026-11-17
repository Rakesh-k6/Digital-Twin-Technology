using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Controls 3-aspect vehicular traffic signal heads and pedestrian crossing indicators.
    /// Responds to normal automatic cycles and power grid blackout/flashing amber failure states.
    /// </summary>
    public class TrafficLightController : MonoBehaviour
    {
        [Header("Signal Identity")]
        public string signalId;
        public string zoneId;
        public string feederId;

        [Header("Light Emitters (Mesh Renderers)")]
        public MeshRenderer redLightRenderer;
        public MeshRenderer yellowLightRenderer;
        public MeshRenderer greenLightRenderer;
        public MeshRenderer pedestrianWalkRenderer;

        [Header("Glow Lights (Point Lights)")]
        public Light redSpotLight;
        public Light yellowSpotLight;
        public Light greenSpotLight;

        [Header("Materials")]
        public Material redOnMat;
        public Material redOffMat;
        public Material yellowOnMat;
        public Material yellowOffMat;
        public Material greenOnMat;
        public Material greenOffMat;
        public Material walkOnMat;
        public Material walkOffMat;

        [Header("Live State")]
        public string operationalStatus = "NORMAL"; // "NORMAL", "FAIL_FLASHING_AMBER", "BLACKOUT"
        public string currentLightState = "RED";     // "RED", "YELLOW", "GREEN", "OFF"
        public bool pedestrianWalk = false;

        public void SetState(string status, string lightColor, bool pedWalk)
        {
            operationalStatus = status;
            currentLightState = lightColor;
            pedestrianWalk = pedWalk;

            UpdateVisuals();
        }

        private void UpdateVisuals()
        {
            // Reset all lights first
            bool redActive = (currentLightState == "RED");
            bool yellowActive = (currentLightState == "YELLOW");
            bool greenActive = (currentLightState == "GREEN");

            if (operationalStatus == "BLACKOUT")
            {
                redActive = false;
                yellowActive = false;
                greenActive = false;
                pedestrianWalk = false;
            }

            // Apply Materials
            if (redLightRenderer != null && redOnMat != null)
                redLightRenderer.material = redActive ? redOnMat : redOffMat;

            if (yellowLightRenderer != null && yellowOnMat != null)
                yellowLightRenderer.material = yellowActive ? yellowOnMat : yellowOffMat;

            if (greenLightRenderer != null && greenOnMat != null)
                greenLightRenderer.material = greenActive ? greenOnMat : greenOffMat;

            if (pedestrianWalkRenderer != null && walkOnMat != null)
                pedestrianWalkRenderer.material = pedestrianWalk ? walkOnMat : walkOffMat;

            // Apply Point Light Emitters for nighttime / atmospheric realism
            if (redSpotLight != null) redSpotLight.enabled = redActive;
            if (yellowSpotLight != null) yellowSpotLight.enabled = yellowActive;
            if (greenSpotLight != null) greenSpotLight.enabled = greenActive;
        }
    }
}
