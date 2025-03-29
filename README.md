# CareerWise
*Empowering career decision-making through data-driven insights and interactive analytics.*

---

## Project Description
CareerWise is a data analytics platform designed to help students, job seekers, and career advisors explore job market trends, analyze skill demands, and benchmark salaries. Built with powerful visualization tools and machine learning capabilities, the platform supports smarter career choices with real-time, evidence-based recommendations.

### Key Use Cases:
- Understand job market trends by location and industry
- Discover high-demand roles and skills
- Benchmark salaries based on role, experience, and geography
- Recommend career paths using AI and predictive analytics

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

1. Clone the repository:
   - git clone [https://github.com/Padmakshi15/Career-Wise.git](https://github.com/Padmakshi15/Career-Wise)
   - cd CareerWise

2. Create and activate a virtual environment:
   - On Windows:
     - python -m venv venv
     - venv\Scripts\activate
   - On macOS/Linux:
     - python3 -m venv venv
     - source venv/bin/activate

3. Install dependencies:
   - pip install -r requirements.txt

---

## Usage

To run the analytics module:
- python analyze.py

To launch the dashboard:
- streamlit run app.py

To test the data model predictions:
- python test_model.py

---

## 📁 Project Structure

EMPLOYMENTANALYTICSDASHBOARD/
├── assets/                       # Images, logos, or UI-related files
├── data/                         # Raw and processed datasets
│   └── Enhanced_JD_Dataset (version 1).csv
├── pages/                        # Modular page components for dashboard
│   ├── ex.py
│   ├── home.py
│   ├── job_market.py
│   ├── reports.py
│   ├── salary_trends.py
│   └── skill_analysis.py
├── static/                       # Static files (CSS, JS if applicable)
├── templates/                    # HTML templates if using Flask/Jinja
├── venv/                         # Virtual environment (not pushed to GitHub)
├── app.py                        # Main application file (entry point)
├── README.md                     # Project overview and usage guide
├── requirements.txt              # List of Python dependencies
└── .gitignore                    # Files/folders to ignore in version control

---

## Features

- Industry-wise salary benchmarking and job role segmentation
- High-demand skills tracking via frequency analysis
- AI-driven career recommendations
- Power BI dashboard with role, location, and skill filters
- Exportable reports for academic and institutional use

---

## 📊 Dashboard Preview

Will add screenshot here

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

Steps to contribute:
1. Fork the repo  
2. Create a feature branch (e.g., git checkout -b feature-name)  
3. Commit your changes  
4. Push to your branch  
5. Create a pull request

---

## License

MIT License. See the [LICENSE](LICENSE) file for details.
