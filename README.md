# EcoFreeze AI: Off-Grid Battery & Thermal Optimizer

### **The Challenge**

In volatile climate zones and off-grid regions (such as sub-Saharan areas), sudden drops in solar irradiance lead to rapid battery depletion. When the power drops, critical cold storage infrastructure fails—risking the spoilage of fresh produce for farmers and essential medicines for local communities.

### **The Solution**

**EcoFreeze AI** is an intelligent simulation engine and edge-input dashboard designed for real-time Energy Management Systems (EMS). It predicts battery depletion trends and thermal instability ahead of time, utilizing custom **AI Guard Logic** to autonomously protect infrastructure when solar reliability wavers.

---

## Key Features

* ** AI Guard Logic (Economy Mode):** Automatically simulates system throttling to `ECONOMY MODE` when low solar radiation is detected. This mitigates deep battery discharges while keeping internal cold storage temperatures stabilized at a safe $4.7^\circ\text{C}$.
* ** 24-Hour Battery Depletion Projection:** Empowers energy engineers to visually audit battery drain trends and catch drops in State of Health (SOH) before reaching a critical infrastructure warning state.
* ** High-Fidelity Virtual Sandboxing:** Allows sustainability researchers to manipulate ambient temperatures and solar metrics to study energy management dynamics instantly—no expensive hardware setups required.

---

##  Tech Stack & Architecture

* **Core Logic & Engine:** Python, Pandas, NumPy
* **Machine Learning:** Scikit-Learn (Predictive Modeling via `.pkl` pipelines)
* **Interactive Interface:** Streamlit Cloud

### Repository Structure

```text
├── app_ecofreeze.py      # Main Streamlit web application dashboard
├── cold_storage.py       # Core logic, conditional rules, and EMS processing
├── ecofreeze_data.csv    # Historical solar, thermal, and battery dataset
├── model_temp.pkl        # Trained model for predicting temperature trends
├── model_discharge.pkl   # Trained model for battery discharge behaviors
└── requirements.txt      # Project dependencies

```

---

##  Behind the Code

> **Development Insight:** Tackling the interdependent conditional logic, reactive status responses, and real-time cross-metric dashboard updates required extensive debugging sessions. Solving those complex edge cases to ensure the simulation behaves reliably under extreme environmental shifts was an incredibly rewarding engineering challenge.

---

##  Getting Started Locally

### 1. Clone the Project

```bash
git clone https://github.com/ecofreeze-ai/Cold_Storage.git
cd Cold_Storage

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Launch the Application

```bash
streamlit run app_ecofreeze.py

```

---

##  Connect & Collaborate

I’m actively working on intersectional AI solutions for GreenTech, energy sustainability, and smart infrastructure. If you find this project interesting or want to discuss optimizations, let's connect!

* **GitHub:** [@ecofreeze-ai](https://github.com/Ftz-AI/ecofreeze-ai.git)
* **Live App:** [Drop a comment or feedback on my interactive live setup!](https://www.linkedin.com/feed/update/urn:li:activity:7465078401826144256?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7465078401826144256%2C7465078789811752960%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287465078789811752960%2Curn%3Ali%3Aactivity%3A7465078401826144256%29)
