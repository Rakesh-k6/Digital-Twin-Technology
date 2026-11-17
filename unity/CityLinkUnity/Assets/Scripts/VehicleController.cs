using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Controls 3D vehicle representation, smooth coordinate interpolation,
    /// wheel spinning physics, brake light illumination, and emergency vehicle sirens.
    /// </summary>
    public class VehicleController : MonoBehaviour
    {
        [Header("Vehicle Identity")]
        public string vehicleId;
        public string vehicleType = "car";
        public bool isEmergency = false;

        [Header("Physical State")]
        public float currentSpeed = 0.0f;
        public bool isBraking = false;
        public bool inQueue = false;

        [Header("Visual Components")]
        public Transform[] wheels;
        public MeshRenderer brakeLightRenderer;
        public Light emergencySirenLight;
        public Material brakeLightActiveMat;
        public Material brakeLightOffMat;

        // Target coordinates from simulation streaming
        private Vector3 targetPosition;
        private Quaternion targetRotation;
        private float sirenTimer = 0.0f;

        void Start()
        {
            targetPosition = transform.position;
            targetRotation = transform.rotation;
        }

        public void UpdateTelemetry(Vector3 newPos, float heading, float speed, bool braking, bool queued, bool siren)
        {
            targetPosition = newPos;
            targetRotation = Quaternion.Euler(0.0f, heading, 0.0f);
            currentSpeed = speed;
            isBraking = braking;
            inQueue = queued;
            isEmergency = siren;
        }

        void Update()
        {
            // Smooth position and rotation interpolation (Dead reckoning)
            float lerpRate = 12.0f;
            transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime * lerpRate);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * lerpRate);

            // Wheel rotation proportional to ground speed
            if (wheels != null && wheels.Length > 0 && currentSpeed > 0.1f)
            {
                float wheelRotationAngle = (currentSpeed / 0.35f) * Mathf.Rad2Deg * Time.deltaTime;
                foreach (Transform wheel in wheels)
                {
                    if (wheel != null)
                    {
                        wheel.Rotate(Vector3.right, wheelRotationAngle, Space.Self);
                    }
                }
            }

            // Brake Light Logic
            if (brakeLightRenderer != null && brakeLightActiveMat != null && brakeLightOffMat != null)
            {
                brakeLightRenderer.material = isBraking ? brakeLightActiveMat : brakeLightOffMat;
            }

            // Emergency Siren Flashing Logic
            if (isEmergency && emergencySirenLight != null)
            {
                sirenTimer += Time.deltaTime * 8.0f;
                emergencySirenLight.enabled = true;
                emergencySirenLight.color = (Mathf.Sin(sirenTimer) > 0.0f) ? Color.red : Color.blue;
                emergencySirenLight.intensity = 3.5f;
            }
            else if (emergencySirenLight != null)
            {
                emergencySirenLight.enabled = false;
            }
        }
    }
}
