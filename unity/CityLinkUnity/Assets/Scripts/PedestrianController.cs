using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Controls 3D pedestrian character models:
    /// - Continuous footpath walking & zebra crossing
    /// - Procedural natural walking animation (alternating arm and leg swing)
    /// - Waiting at road crossings when pedestrian signal is RED
    /// </summary>
    public class PedestrianController : MonoBehaviour
    {
        [Header("Identity & State")]
        public string pedestrianId;
        public string zoneId;
        public string walkingState = "WALKING"; // "WALKING", "WAITING_CROSSING", "CROSSING"
        public float speed = 1.3f;

        [Header("Procedural Rigging Joints")]
        public Transform leftLeg;
        public Transform rightLeg;
        public Transform leftArm;
        public Transform rightArm;

        private Vector3 targetPosition;
        private Quaternion targetRotation;
        private float walkCycleTime = 0.0f;

        void Start()
        {
            targetPosition = transform.position;
            targetRotation = transform.rotation;
        }

        public void UpdateTelemetry(Vector3 newPos, float heading, string state)
        {
            targetPosition = newPos;
            targetRotation = Quaternion.Euler(0.0f, heading, 0.0f);
            walkingState = state;
        }

        void Update()
        {
            // Smooth movement interpolation
            transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime * 10.0f);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * 10.0f);

            bool isMoving = (walkingState != "WAITING_CROSSING");

            // Procedural walking gait animation
            if (isMoving)
            {
                walkCycleTime += Time.deltaTime * speed * 7.0f;
                float swingAngle = Mathf.Sin(walkCycleTime) * 28.0f;

                if (leftLeg != null) leftLeg.localRotation = Quaternion.Euler(swingAngle, 0, 0);
                if (rightLeg != null) rightLeg.localRotation = Quaternion.Euler(-swingAngle, 0, 0);
                if (leftArm != null) leftArm.localRotation = Quaternion.Euler(-swingAngle * 0.8f, 0, 0);
                if (rightArm != null) rightArm.localRotation = Quaternion.Euler(swingAngle * 0.8f, 0, 0);
            }
            else
            {
                // Standing idle posture while waiting for green signal
                if (leftLeg != null) leftLeg.localRotation = Quaternion.identity;
                if (rightLeg != null) rightLeg.localRotation = Quaternion.identity;
                if (leftArm != null) leftArm.localRotation = Quaternion.identity;
                if (rightArm != null) rightArm.localRotation = Quaternion.identity;
            }
        }
    }
}
