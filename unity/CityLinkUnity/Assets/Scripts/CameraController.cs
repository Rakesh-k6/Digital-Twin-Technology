using UnityEngine;

namespace CityLink
{
    /// <summary>
    /// Multi-mode camera controller for the CityLink 3D Virtual City.
    /// Supports:
    /// 1. Free-Roam (WASD + Mouse Look + Q/E Height)
    /// 2. Top-View (Overhead Orthographic / Isometric Satellite view)
    /// 3. Follow-Vehicle (Attaches to selected active vehicle or emergency vehicle)
    /// 4. Scroll-wheel Zoom & Speed adjustment
    /// </summary>
    public class CameraController : MonoBehaviour
    {
        public enum CameraMode
        {
            FreeRoam,
            TopView,
            FollowVehicle
        }

        [Header("Mode & Target")]
        public CameraMode currentMode = CameraMode.FreeRoam;
        public Transform targetVehicle = null;

        [Header("Movement Speeds")]
        public float moveSpeed = 40.0f;
        public float fastMultiplier = 2.5f;
        public float mouseSensitivity = 2.5f;
        public float zoomSpeed = 25.0f;

        [Header("Top-View Settings")]
        public Vector3 topViewPosition = new Vector3(0.0f, 180.0f, 0.0f);
        public Vector3 topViewRotation = new Vector3(90.0f, 0.0f, 0.0f);

        [Header("Follow Settings")]
        public Vector3 followOffset = new Vector3(0.0f, 6.0f, -12.0f);
        public float followSmoothness = 6.0f;

        private float pitch = 45.0f;
        private float yaw = 0.0f;

        void Start()
        {
            // Initial camera placement overlooking the 4 zones
            if (currentMode == CameraMode.FreeRoam)
            {
                transform.position = new Vector3(0.0f, 90.0f, -160.0f);
                pitch = 30.0f;
                yaw = 0.0f;
                transform.rotation = Quaternion.Euler(pitch, yaw, 0.0f);
            }
        }

        void Update()
        {
            // Mode switching shortcuts
            if (Input.GetKeyDown(KeyCode.Alpha1)) SwitchMode(CameraMode.FreeRoam);
            if (Input.GetKeyDown(KeyCode.Alpha2)) SwitchMode(CameraMode.TopView);
            if (Input.GetKeyDown(KeyCode.Alpha3)) SwitchMode(CameraMode.FollowVehicle);

            switch (currentMode)
            {
                case CameraMode.FreeRoam:
                    HandleFreeRoam();
                    break;
                case CameraMode.TopView:
                    HandleTopView();
                    break;
                case CameraMode.FollowVehicle:
                    HandleFollowVehicle();
                    break;
            }
        }

        public void SwitchMode(CameraMode newMode)
        {
            currentMode = newMode;
            if (currentMode == CameraMode.TopView)
            {
                transform.position = topViewPosition;
                transform.rotation = Quaternion.Euler(topViewRotation);
            }
        }

        private void HandleFreeRoam()
        {
            // Right-click or middle-click mouse orbit
            if (Input.GetMouseButton(1))
            {
                yaw += Input.GetAxis("Mouse X") * mouseSensitivity;
                pitch -= Input.GetAxis("Mouse Y") * mouseSensitivity;
                pitch = Mathf.Clamp(pitch, -85.0f, 85.0f);
                transform.rotation = Quaternion.Euler(pitch, yaw, 0.0f);
            }

            float speed = moveSpeed * (Input.GetKey(KeyCode.LeftShift) ? fastMultiplier : 1.0f);

            // WASD Horizontal Movement
            float h = Input.GetAxis("Horizontal"); // A/D
            float v = Input.GetAxis("Vertical");   // W/S

            Vector3 moveDir = transform.forward * v + transform.right * h;
            moveDir.y = 0.0f; // Stay horizontal
            if (moveDir.sqrMagnitude > 0.01f) moveDir.Normalize();

            // Q / E for Vertical Height elevation
            float up = 0.0f;
            if (Input.GetKey(KeyCode.E)) up += 1.0f;
            if (Input.GetKey(KeyCode.Q)) up -= 1.0f;

            transform.position += (moveDir * speed + Vector3.up * (up * speed)) * Time.deltaTime;

            // Scroll Wheel Zoom
            float scroll = Input.GetAxis("Mouse ScrollWheel");
            if (Mathf.Abs(scroll) > 0.01f)
            {
                transform.position += transform.forward * (scroll * zoomSpeed * 10.0f);
            }
        }

        private void HandleTopView()
        {
            // WASD Pan in 2D Plane
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            Vector3 pan = new Vector3(h, 0.0f, v) * (moveSpeed * 1.5f * Time.deltaTime);
            transform.position += pan;

            // Scroll Zoom Height
            float scroll = Input.GetAxis("Mouse ScrollWheel");
            if (Mathf.Abs(scroll) > 0.01f)
            {
                transform.position += Vector3.down * (scroll * zoomSpeed * 15.0f);
                // Clamp height
                transform.position = new Vector3(transform.position.x, Mathf.Clamp(transform.position.y, 40.0f, 350.0f), transform.position.z);
            }
        }

        private void HandleFollowVehicle()
        {
            if (targetVehicle == null)
            {
                // Auto-find emergency vehicle or first vehicle in scene
                VehicleController veh = FindObjectOfType<VehicleController>();
                if (veh != null) targetVehicle = veh.transform;
            }

            if (targetVehicle != null)
            {
                Vector3 targetPos = targetVehicle.position + targetVehicle.TransformDirection(followOffset);
                transform.position = Vector3.Lerp(transform.position, targetPos, Time.deltaTime * followSmoothness);

                Quaternion targetRot = Quaternion.LookRotation(targetVehicle.position - transform.position);
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRot, Time.deltaTime * followSmoothness);
            }
        }
    }
}
