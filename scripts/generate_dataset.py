"""
Generates the synthetic dataset used in this project:
data/India_Student_Performance_Placement_50K.csv

50,000 student records modelled on Indian higher-education patterns
(17 states, ~150 colleges, 9 courses, admission years 2019-2025).
Relationships are built in on purpose (attendance -> CGPA -> placement,
backlogs -> dropout, college tier / specialization -> package) so the
dashboard shows realistic insights. The data is NOT real student data.

Usage (Python 3, standard library only):
    python scripts/generate_dataset.py data/India_Student_Performance_Placement_50K.csv
"""
import csv, random, sys

random.seed(2026)
N = 50000
out = sys.argv[1] if len(sys.argv) > 1 else "India_Student_Performance_Placement_50K.csv"

states = {
    "Maharashtra": (["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"], 14),
    "Karnataka": (["Bengaluru", "Mysuru", "Mangaluru", "Hubballi"], 11),
    "Tamil Nadu": (["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli"], 12),
    "Uttar Pradesh": (["Lucknow", "Noida", "Kanpur", "Varanasi", "Prayagraj"], 13),
    "Telangana": (["Hyderabad", "Warangal"], 8),
    "Delhi": (["New Delhi"], 7),
    "West Bengal": (["Kolkata", "Durgapur", "Siliguri"], 7),
    "Gujarat": (["Ahmedabad", "Surat", "Vadodara", "Rajkot"], 7),
    "Rajasthan": (["Jaipur", "Kota", "Jodhpur", "Udaipur"], 6),
    "Kerala": (["Kochi", "Thiruvananthapuram", "Kozhikode"], 5),
    "Madhya Pradesh": (["Bhopal", "Indore", "Gwalior"], 5),
    "Andhra Pradesh": (["Visakhapatnam", "Vijayawada", "Tirupati"], 5),
    "Punjab": (["Chandigarh", "Ludhiana", "Amritsar"], 3),
    "Bihar": (["Patna", "Gaya"], 3),
    "Odisha": (["Bhubaneswar", "Cuttack"], 3),
    "Haryana": (["Gurugram", "Faridabad"], 3),
    "Assam": (["Guwahati"], 2),
}
state_names = list(states)
state_w = [states[s][1] for s in state_names]

# course: (specializations, duration yrs, base annual fee INR, placement base rate, avg package LPA)
courses = {
    "B.Tech": (["Computer Science", "Information Technology", "Electronics & Communication",
                "Mechanical", "Civil", "Electrical", "AI & Data Science"], 4, 150000, 0.72, 6.5),
    "BCA": (["Computer Applications"], 3, 70000, 0.55, 3.8),
    "B.Sc": (["Physics", "Chemistry", "Mathematics", "Computer Science", "Biotechnology"], 3, 40000, 0.35, 3.2),
    "B.Com": (["General", "Accounting & Finance", "Banking & Insurance"], 3, 35000, 0.45, 3.4),
    "BBA": (["Marketing", "Finance", "Human Resources"], 3, 90000, 0.52, 4.0),
    "BA": (["Economics", "English", "Psychology", "Political Science"], 3, 25000, 0.25, 2.8),
    "MBA": (["Marketing", "Finance", "Human Resources", "Business Analytics", "Operations"], 2, 250000, 0.80, 9.0),
    "MCA": (["Computer Applications"], 2, 110000, 0.68, 5.5),
    "M.Tech": (["Computer Science", "VLSI Design", "Structural Engineering", "Data Science"], 2, 120000, 0.70, 8.0),
}
course_names = list(courses)
course_w = [26, 10, 13, 12, 8, 9, 10, 6, 6]
spec_bonus = {"Computer Science": 1.35, "AI & Data Science": 1.4, "Information Technology": 1.25,
              "Business Analytics": 1.3, "Data Science": 1.35, "Finance": 1.1,
              "Civil": 0.8, "Mechanical": 0.85}

# colleges per state: (name, type, tier)
prefixes = ["Government", "Sri", "St. Xavier's", "Global", "Apex", "Saraswati",
            "Vivekananda", "Royal", "City", "Pioneer", "Modern"]
suffixes = ["Institute of Technology", "College of Engineering", "Arts & Science College",
            "Institute of Management", "University", "College"]
colleges = {}
cid = 0
for s in state_names:
    lst = []
    for city in states[s][0]:
        for _ in range(random.randint(2, 4)):
            cid += 1
            ctype = random.choices(["Government", "Private", "Deemed University", "Autonomous"],
                                   [30, 45, 10, 15])[0]
            p = "Government" if ctype == "Government" else random.choice(prefixes[1:])
            name = f"{p} {random.choice(suffixes)}, {city}"
            tier = random.choices([1, 2, 3], [15, 40, 45])[0]
            lst.append((f"C{cid:03d}", name, ctype, tier, city))
    colleges[s] = lst

first_m = ["Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Karan", "Rahul", "Siddharth", "Ishaan",
           "Yash", "Pranav", "Harsh", "Nikhil", "Amit", "Vikram", "Sai", "Kiran", "Manish",
           "Abhishek", "Rajesh", "Mohammed", "Farhan", "Gurpreet", "Ankit", "Deepak", "Suresh", "Ravi"]
first_f = ["Ananya", "Diya", "Priya", "Sneha", "Kavya", "Isha", "Pooja", "Neha", "Riya", "Aditi",
           "Shruti", "Meera", "Lakshmi", "Divya", "Anjali", "Nisha", "Sana", "Fatima", "Harleen",
           "Tanvi", "Swati", "Pallavi", "Keerthi", "Bhavya", "Aishwarya", "Sakshi"]
last = ["Sharma", "Verma", "Patel", "Reddy", "Iyer", "Nair", "Gupta", "Singh", "Kumar", "Das",
        "Joshi", "Mehta", "Rao", "Khan", "Chatterjee", "Banerjee", "Pillai", "Yadav", "Mishra",
        "Agarwal", "Deshmukh", "Kulkarni", "Shetty", "Menon", "Bose", "Gill", "Naidu", "Jain"]

companies = {
    "IT Services": ["TCS", "Infosys", "Wipro", "HCLTech", "Tech Mahindra", "Cognizant"],
    "Product / Tech": ["Google", "Microsoft", "Amazon", "Flipkart", "Zoho", "Freshworks"],
    "Banking & Finance": ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Deloitte", "KPMG"],
    "Core Engineering": ["L&T", "Tata Motors", "Mahindra", "BHEL", "Siemens"],
    "FMCG / Retail": ["HUL", "ITC", "Reliance Retail", "Nestle India"],
    "Startup": ["Startup"],
}

def clamp(x, lo, hi): return max(lo, min(hi, x))

cols = ["Student_ID", "Student_Name", "Gender", "Age", "Date_of_Birth", "State", "City", "Region",
        "College_ID", "College_Name", "College_Type", "College_Tier", "Course", "Specialization",
        "Admission_Year", "Graduation_Year", "Category", "Area_Type", "Family_Annual_Income_INR",
        "Tenth_Percentage", "Twelfth_Percentage", "Entrance_Score", "Attendance_Percentage",
        "CGPA", "Backlogs", "Annual_Fee_INR", "Scholarship", "Scholarship_Amount_INR",
        "Hostel_Resident", "Internships_Done", "Certifications", "Extracurricular",
        "Study_Status", "Placement_Status", "Company_Sector", "Company_Name", "Package_LPA"]
region = {"Maharashtra": "West", "Gujarat": "West", "Rajasthan": "West", "Karnataka": "South",
          "Tamil Nadu": "South", "Telangana": "South", "Kerala": "South", "Andhra Pradesh": "South",
          "Uttar Pradesh": "North", "Delhi": "North", "Punjab": "North", "Haryana": "North",
          "Madhya Pradesh": "Central", "West Bengal": "East", "Bihar": "East", "Odisha": "East",
          "Assam": "North-East"}

with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for i in range(1, N + 1):
        g = random.choices(["Male", "Female", "Other"], [54, 45.6, 0.4])[0]
        fn = random.choice(first_f if g == "Female" else first_m)
        name = f"{fn} {random.choice(last)}"
        st = random.choices(state_names, state_w)[0]
        col = random.choice(colleges[st])
        crs = random.choices(course_names, course_w)[0]
        specs, dur, fee_base, pl_base, pkg_base = courses[crs]
        spec = random.choice(specs)
        adm = random.choices([2019, 2020, 2021, 2022, 2023, 2024, 2025], [10, 12, 14, 16, 16, 16, 16])[0]
        grad = adm + dur
        pg = crs in ("MBA", "MCA", "M.Tech")
        age_at_adm = random.randint(21, 24) if pg else random.randint(17, 19)
        age = clamp(2026 - adm + age_at_adm, 17, 35)
        dob = f"{adm - age_at_adm}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        cat = random.choices(["General", "OBC", "SC", "ST", "EWS"], [38, 34, 14, 7, 7])[0]
        area = random.choices(["Urban", "Semi-Urban", "Rural"], [45, 25, 30])[0]
        inc_mu = {"Urban": 900000, "Semi-Urban": 550000, "Rural": 320000}[area]
        if cat in ("SC", "ST"): inc_mu *= 0.7
        income = int(clamp(random.lognormvariate(0, 0.55) * inc_mu, 60000, 6000000) // 1000 * 1000)
        ability = random.gauss(0, 1)
        t10 = round(clamp(76 + 9 * ability + random.gauss(0, 5), 40, 99.6), 1)
        t12 = round(clamp(t10 + random.gauss(-2, 5), 40, 99.4), 1)
        entr = round(clamp(55 + 15 * ability + (4 - col[3]) * 5 + random.gauss(0, 8), 5, 100), 1)
        att = round(clamp(78 + 6 * ability + random.gauss(0, 9) + (3 if g == "Female" else 0), 35, 100), 1)
        cgpa = round(clamp(6.9 + 0.8 * ability + (att - 78) * 0.025 + random.gauss(0, 0.45), 4.0, 9.95), 2)
        backlogs = 0 if cgpa > 7.5 else min(8, int(random.expovariate(1 / max(0.3, (7.5 - cgpa) * 2))))
        tier_fee = {1: 1.6, 2: 1.0, 3: 0.75}[col[3]]
        type_fee = {"Government": 0.35, "Private": 1.2, "Deemed University": 1.6, "Autonomous": 1.0}[col[2]]
        fee = int(fee_base * tier_fee * type_fee * random.uniform(0.85, 1.15) // 500 * 500)
        sch_p = 0.12 + (0.35 if cat in ("SC", "ST") else 0.15 if cat in ("OBC", "EWS") else 0) \
                + (0.2 if income < 300000 else 0) + (0.15 if cgpa > 8.5 else 0)
        sch = random.random() < clamp(sch_p, 0, 0.9)
        sch_amt = int(fee * random.uniform(0.25, 1.0) // 500 * 500) if sch else 0
        hostel = "Yes" if random.random() < (0.55 if area != "Urban" else 0.25) else "No"
        interns = min(4, int(random.expovariate(1 / (0.6 + 0.4 * max(0, ability) + (0.5 if pg else 0)))))
        certs = min(8, int(random.expovariate(1 / (1.2 + 0.6 * max(0, ability)))))
        extra = random.choices(["Sports", "Cultural", "Technical Club", "NSS/NCC", "None"], [18, 16, 20, 12, 34])[0]

        # status
        if grad <= 2026:
            drop_p = 0.03 + (0.12 if backlogs >= 3 else 0) + (0.05 if income < 200000 else 0)
            status = "Dropped Out" if random.random() < drop_p else "Graduated"
        else:
            drop_p = 0.015 + (0.06 if backlogs >= 3 else 0)
            status = "Dropped Out" if random.random() < drop_p else "Currently Studying"

        placement, sector, comp, pkg = "Not Applicable", "", "", ""
        if status == "Graduated":
            p = pl_base * spec_bonus.get(spec, 1.0) ** 0.5 + (cgpa - 7) * 0.08 + interns * 0.05 \
                + certs * 0.01 - backlogs * 0.06 + {1: 0.12, 2: 0.0, 3: -0.1}[col[3]] \
                + (-0.15 if grad == 2021 else 0)  # covid batch
            if random.random() < clamp(p, 0.03, 0.97):
                placement = "Placed"
                if crs in ("B.Tech", "BCA", "MCA", "M.Tech") or "Computer" in spec or "Data" in spec:
                    sw = [45, 15, 8, 18, 2, 12]
                elif crs in ("B.Com", "MBA", "BBA"):
                    sw = [12, 6, 42, 2, 25, 13]
                else:
                    sw = [25, 3, 25, 5, 22, 20]
                sector = random.choices(list(companies), sw)[0]
                comp = random.choice(companies[sector])
                mult = {"Product / Tech": 2.6, "Banking & Finance": 1.2, "Core Engineering": 1.0,
                        "IT Services": 0.75, "FMCG / Retail": 1.15, "Startup": 1.1}[sector]
                pkg = pkg_base * mult * spec_bonus.get(spec, 1.0) * {1: 1.5, 2: 1.0, 3: 0.78}[col[3]] \
                      * (1 + (cgpa - 7) * 0.08) * random.lognormvariate(0, 0.22)
                pkg = round(clamp(pkg, 1.8, 48), 2)
            else:
                placement = random.choices(["Not Placed", "Higher Studies"], [70, 30])[0]

        w.writerow([f"STU{i:06d}", name, g, age, dob, st, col[4], region[st], col[0], col[1], col[2],
                    f"Tier {col[3]}", crs, spec, adm, grad, cat, area, income, t10, t12, entr, att,
                    cgpa, backlogs, fee, "Yes" if sch else "No", sch_amt, hostel, interns, certs,
                    extra, status, placement, sector, comp, pkg])
print("done")
