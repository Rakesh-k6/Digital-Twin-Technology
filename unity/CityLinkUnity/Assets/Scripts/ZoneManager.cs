using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Manages the 4 interconnected urban zones:
    /// - Zone A: Koramangala
    /// - Zone B: HSR Layout
    /// - Zone C: Bellandur
    /// - Zone D: Silk Board
    /// Displays zone boundary projection, floating holographic HUD title, and live congestion heat tint.
    /// </summary>
    public class ZoneManager : MonoBehaviour
    {
        [System.Serializable]
        public class ZoneHUD
        {
            public string zoneId;
            public string zoneName;
            public Vector3 center;
            public TextMesh labelMesh;
            public MeshRenderer groundBoundaryRenderer;
        }

        public ZoneHUD[] zones;

        public void UpdateZoneDensities(string zoneId, float density)
        {
            foreach (var z in zones)
            {
                if (z.zoneId == zoneId)
                {
                    // Tint ground boundary based on congestion
                    Color heat = Color.Lerp(new Color(0.2f, 0.6f, 1.0f, 0.25f), new Color(1.0f, 0.1f, 0.1f, 0.5f), density);
                    if (z.groundBoundaryRenderer != null)
                    {
                        z.groundBoundaryRenderer.material.color = heat;
                    }

                    if (z.labelMesh != null)
                    {
                        z.labelMesh.text = $"{z.zoneName}\nDensity: {(density * 100.0f):F0}%";
                    }
                }
            }
        }
    }
}
