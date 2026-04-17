const APOLLO_CONFIG = {
  defaultInferenceApi: ""
};

const APOLLO_STUDENTS = [
  {
    id: "aarthika-birajdar",
    name: "Aarthika Birajdar",
    email: "aarthikabirajdar@gmail.com",
    role: "Group Lead and Project Coordination",
    focus: "End-to-end project direction and integration",
    affiliation: "Shri Siddheshwar Women's Polytechnic, Solapur",
    delivery: "Cross-functional coordination for integrated paper, website, and product tracks"
  },
  {
    id: "siddheshwari-degaonkar",
    name: "Siddheshwari Degaonkar",
    email: "degaonkarsiddehswhari@gmail.com",
    role: "Frontend Development",
    focus: "User interface and presentation workflows",
    affiliation: "Shri Siddheshwar Women's Polytechnic, Solapur",
    delivery: "Design and UX workflows for user-facing product interfaces"
  },
  {
    id: "vaishnavi-dhuttarge",
    name: "Vaishnavi Dhuttarge",
    email: "vaishnavidhuttarge26@gmail.com",
    role: "IoT and Sensors",
    focus: "Telemetry capture and field sensing",
    affiliation: "Shri Siddheshwar Women's Polytechnic, Solapur",
    delivery: "Sensor integrations and telemetry stream mapping"
  },
  {
    id: "anuja-gurav",
    name: "Anuja Gurav",
    email: "anujamg23@gmail.com",
    role: "Robotics and ROS",
    focus: "Robot orchestration and motion stack",
    affiliation: "Shri Siddheshwar Women's Polytechnic, Solapur",
    delivery: "Robotics and ROS module direction for autonomous mobility"
  },
  {
    id: "ojausvi-bhave",
    name: "Ojausvi Bhave",
    email: "ojausvibhave@gmail.com",
    role: "Database Management",
    focus: "Data persistence, labeling and retrieval",
    affiliation: "Shri Siddheshwar Women's Polytechnic, Solapur",
    delivery: "Database layer readiness for model and field data workflows"
  },
  {
    id: "sharvari-garad",
    name: "Sharvari Garad",
    email: "sharvarigarad03@gmail.com",
    role: "Research and Database",
    focus: "Research documentation and dataset quality",
    affiliation: "Shri Siddheshwar Women's Polytechnic, Solapur",
    delivery: "Research quality control, documentation depth, and data consistency"
  }
];

const APOLLO_TECH = [
  {
    id: "cnn-disease-intelligence",
    name: "CNN Disease Intelligence",
    stack: "TensorFlow / Keras",
    capability: "Crop disease classification and severity estimation",
    roadmap: "Move from static classification to temporal health progression modeling",
    status: "Active, integrated in inference workspace",
    demoUrl: "index.html#inference"
  },
  {
    id: "yolo-leaf-localization",
    name: "YOLO Leaf Localization",
    stack: "YOLOv8",
    capability: "Leaf and crop region detection for robust downstream inference",
    roadmap: "Edge deployment with pruning and quantization for low-latency field devices",
    status: "Validated in reference backend",
    demoUrl: "index.html#inference"
  },
  {
    id: "ros2-robotics-core",
    name: "ROS2 Robotics Core",
    stack: "ROS2",
    capability: "Distributed robotics messaging, autonomy and coordination",
    roadmap: "Mission planner for multi-robot field fleets",
    status: "Roadmap, architecture defined",
    demoUrl: ""
  },
  {
    id: "iot-sensor-fusion",
    name: "IoT Sensor Fusion",
    stack: "Telemetry and sensor integration",
    capability: "Realtime weather, moisture, and environment data ingestion",
    roadmap: "Closed-loop agronomy recommendation engine",
    status: "Live weather node active",
    demoUrl: "index.html#ops"
  },
  {
    id: "dashboard-frontend",
    name: "Dashboard Frontend",
    stack: "React and web UI",
    capability: "Farmer-facing and research-facing operational dashboards",
    roadmap: "Role-based views for students, researchers, and farm operators",
    status: "Active and visible in command center",
    demoUrl: "index.html#ops"
  },
  {
    id: "data-backend-api",
    name: "Data and Inference API",
    stack: "FastAPI",
    capability: "Unified API for detection, reports, and telemetry",
    roadmap: "Containerized deployment and autoscaled inference services",
    status: "Ready for endpoint wiring",
    demoUrl: "index.html#inference"
  },
  {
    id: "autonomous-rover-track",
    name: "Autonomous Rover Track",
    stack: "Robotics and control",
    capability: "Field navigation for distributed sensing and intervention",
    roadmap: "Semi-autonomous to fully autonomous operation on irregular terrain",
    status: "Prototype roadmap",
    demoUrl: ""
  },
  {
    id: "autonomous-lander-track",
    name: "Autonomous Lander Track",
    stack: "Advanced mobility and manipulation",
    capability: "High-precision docking and task execution in constrained spaces",
    roadmap: "Harvest manipulation for delicate crop categories",
    status: "Future expansion program",
    demoUrl: ""
  }
];

const APOLLO_STATUS_STREAM = [
  { module: "Inference API Bridge", level: "ok" },
  { module: "Weather Telemetry", level: "ok" },
  { module: "Robotics Mission Planner", level: "warn" },
  { module: "Multi-Plot Sync", level: "ok" },
  { module: "Crop Risk Alert Engine", level: "warn" },
  { module: "Autonomous Rover Ops", level: "error" }
];