# 🛡️ Compromised EC2 Response Simulator

A security-focused automation tool that simulates incident response workflows for compromised EC2 instances using Python, Flask, and Boto3. Built during my internship at Experian, this project reflects my understanding of AWS security operations, automation, and risk mitigation.

---

## 📌 Key Features

* ✅ Tag EC2 instances as "Compromised"
* 🔄 Disassociate public IPs from the instance
* 🌐 Remove from Application Load Balancers
* 🔐 Apply quarantine Security Groups
* 📅 Create forensic EBS snapshots
* 🕸️ Move instance to isolated subnet

---

## 🧰 Tech Stack

| Component | Details          |
| --------: | :--------------- |
|   Backend | Python 3 + Flask |
|   AWS SDK | Boto3            |
|  Frontend | HTML + Jinja2    |
|     Cloud | AWS EC2          |

---

## 🚀 Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/compromised_ec2_response_simulator.git
cd compromised_ec2_response_simulator
```

2. **Set up the virtual environment**

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up AWS credentials**

Use environment variables or your local `~/.aws/credentials` file.

5. **Run the app**

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## 🛁 Project Structure

```
compromised_ec2_response_simulator/
├── app.py               # Flask entry point
├── routes/              # Route handlers (response logic)
├── utils/               # Boto3 AWS helper functions
├── templates/           # HTML UI (Jinja2)
├── requirements.txt     # Python dependencies
└── .gitignore
```

---

## 🧠 Learning Outcomes

* Implemented real-world incident response flows on AWS
* Gained hands-on experience with Boto3 and EC2 configurations
* Used Flask routing and Blueprint modularization
* Reinforced understanding of EC2 networking, tagging, and IAM permissions

---

## 🔐 Security Notes

* Do **not** hardcode AWS credentials.
* Use IAM roles or environment-based configuration.
* Ensure the EC2 instances and actions are run in a test or non-production environment.


---

## 📳 Acknowledgments

Developed as a side project during my **IT Audit Internship at Experian** as part of training and exploration of AWS security automation.

---

## 📌 License

This project is open-sourced under the [MIT License](LICENSE).
