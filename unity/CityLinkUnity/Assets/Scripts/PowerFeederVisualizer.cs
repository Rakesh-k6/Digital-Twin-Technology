using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Visualizes 11kV electrical feeders, transmission lines, and zone power flow.
    /// Displays color-coded loading:
    /// - Green: Normal (< 85%)
    /// - Yellow: Warning (85% - 100%)
    /// - Red: Overloaded (> 100%)
    /// - Grey: Tripped / Blackout
    /// </summary>
    public class PowerFeederVisualizer : MonoBehaviour
    {
        [Header("Feeder Identity")]
        public string feederId;
        public string zoneName;
        public float capacityMW;

        [Header("Visual Mesh & Materials")]
        public LineRenderer powerConduitLine;
        public MeshRenderer transformerRenderer;
        public Light substationGlowLight;

        public Material normalMat;     // Glowing Green
        public Material warningMat;    // Glowing Yellow
        public Material overloadedMat; // Glowing Red
        public Material trippedMat;    // Matte Dark Grey

        [Header("Live Metrics")]
        public float currentLoadMW = 0.0f;
        public float loadingPercentage = 0.0f;
        public string feederStatus = "NORMAL";
        public bool isBreakerClosed = true;

        public void UpdateFeederState(float loadMW, float percentage, string status, bool breakerClosed)
        {
            currentLoadMW = loadMW;
            loadingPercentage = percentage;
            feederStatus = status;
            isBreakerClosed = breakerClosed;

            Material targetMat = normalMat;
            Color glowColor = Color.green;

            if (!isBreakerClosed || feederStatus == "TRIPPED")
            {
                targetMat = trippedMat;
                glowColor = Color.gray;
            }
            else if (feederStatus == "OVERLOADED")
            {
                targetMat = overloadedMat;
                glowColor = Color.red;
            }
            else if (feederStatus == "WARNING")
            {
                targetMat = warningMat;
                glowColor = Color.yellow;
            }

            if (transformerRenderer != null && targetMat != null)
            {
                transformerRenderer.material = targetMat;
            }

            if (powerConduitLine != null && targetMat != null)
            {
                powerConduitLine.material = targetMat;
            }

            if (substationGlowLight != null)
            {
                substationGlowLight.color = glowColor;
                substationGlowLight.intensity = (!isBreakerClosed) ? 0.2f : 2.5f;
            }
        }
    }
}
