NetVigilant AI- Explainable Network Anomaly Detection System

NetVigilant AI is an Explainable AI based network anomaly detection platform designed to detect suspicious network behavior, 
explain why an alert occurred, visualize attack progression, and simulate analyst decisions through an interactive dashboard.
This project is built to resemble real-world SOC (Security Operations Center) workflows and is suitable for portfolios, 
internships and entry-level roles in Data Analytics, Cybersecurity, and AI/ML.
--------------------------------------------------

Key Features

- Machine Learning based anomaly detection
- Explainable AI (human readable alert explanations)
- Interactive visualizations
- Scatter plot for normal vs anomaly detection
- Line charts for traffic trends
- Attack timeline reconstruction per source
- Decision simulation (Ignore, Monitor, Quarantine)
- Analyst feedback loop with false positive tracking
- Batch processing and simulated streaming mode
- Deployment ready (Render compatible)

--------------------------------------------------

Project Architecture

NetVigilantAI/
|
|-- netvigilant_ai/
|   |-- data_ingestion/        CSV validation and loading
|   |-- ml/                    Anomaly detection engine
|   |-- explainability/        Explanation logic
|   |-- storyline/             Attack timeline builder
|   |-- streaming/             Streaming simulation
|   |-- decision/              Decision simulation engine
|   |-- feedback/              Feedback logging and metrics
|
|-- sample_data/               Test datasets
|-- app.py                     Streamlit dashboard
|-- feedback_log.csv           Analyst feedback storage
|-- requirements.txt
|-- README.md

--------------------------------------------------

Tech Stack

Language      : Python  
Framework     : Streamlit  
Data & ML     : Pandas, NumPy, Scikit-learn  
Visualization : Streamlit Charts, Matplotlib  
Deployment    : Render  
Version Control : Git and GitHub  

--------------------------------------------------

Dataset

The system uses CSV-based network traffic data.

Typical fields include:
- timestamp
- protocol
- duration
- src_bytes
- dst_bytes
- count
- srv_count
- source_id

The project supports noisy and semi-structured datasets for realistic testing.

--------------------------------------------------

How to Run Locally

1. Clone the repository

git clone https://github.com/your-username/NetVigilantAI.git  
cd NetVigilantAI  

2. Create and activate virtual environment

python -m venv venv  

Windows:
venv\Scripts\activate  

Linux/Mac:
source venv/bin/activate  

3. Install dependencies

pip install -r requirements.txt  

4. Run the application

streamlit run app.py  

--------------------------------------------------

How NetVigilant AI Is Different
 
Unlike typical network anomaly detection projects that only flag suspicious traffic, 
NetVigilant AI focuses on explainability and analyst workflows.
Provides human-readable explanations for why traffic is anomalous (not a black box)
Builds attack timelines by correlating anomalies per source. 
Simulates real SOC decisions (Ignore, Monitor, Quarantine)
Includes a feedback loop to track false positives
Supports batch and near-real-time (streamed) analysis
Uses clear visualizations (scatter & trend plots) instead of misleading charts
Designed with a modular, production-style architecture
NetVigilant AI goes beyond detection by combining Explainable AI, investigation timelines, and 
analyst decision simulation — making it closer to real-world SOC systems than typical student projects.

--------------------------------------------------
Dashboard Modules

1. CSV Upload and Validation  
2. Anomaly Detection Engine  
3. Summary Metrics  
4. Visual Analysis  
5. Explanation Panel (XAI)  
6. Attack Timeline  
7. Decision Simulation  
8. Feedback Loop  

--------------------------------------------------

Use Cases

- Security Operations Center demonstrations
- Cybersecurity learning projects
- Explainable AI research
- Data analytics portfolios

--------------------------------------------------

Limitations

- Uses CSV data instead of live packet capture
- Streaming is simulated using chunks
- Model retraining is not automated yet

--------------------------------------------------

Future Enhancements

- Real-time network packet capture
- Model retraining using analyst feedback
- SIEM and firewall integration
- Advanced deep learning models
- Role-based access control

--------------------------------------------------

Author

Himanjali Chauhan  
Aspiring Data Analyst | AI and Cybersecurity Enthusiast  

--------------------------------------------------

If you like this project, consider starring the repository on GitHub.
