from pii_masker import PIIMasker  # Assuming the PIIMasker class is saved in a file named piimasker.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    input: str

names = [
    "Addison Moore", "Brandon Davis", "Chloe Foster", "Dylan Anderson", "Emily Parker", "Gavin Wilson", "Harper Martin", "Isaac Clark", "Jessica Taylor", "Kylie Adams",
    "Leo Smith", "Madison Young", "Nathan Harris", "Olivia King", "Peyton Mitchell", "Quinn Turner", "Riley Brown", "Savannah Lewis", "Tyler White", "Victoria Garcia",
    "Wyatt Martinez", "Zoe Turner", "Alexander Moore", "Bella Carter", "Cameron Davis", "Daniel Thompson", "Ella Wilson", "Finn Robinson", "Grace Turner", "Henry Baker",
    "Isabella Harris", "Jack Lewis", "Kayla White", "Liam Adams", "Mia Hernandez", "Nathan King", "Olivia Allen", "Parker Scott", "Quinn Anderson", "Riley Carter",
    "Sophia Baker", "Thomas Evans", "Ulysses Foster", "Victoria Garcia", "William Hall", "Xander Jackson", "Yasmine Lopez", "Zoey Martinez", "Ava Perez", "Benjamin Smith",
    "Caleb Turner", "Daisy Harris", "Elijah Wilson", "Faith Thompson", "Gabriel Green", "Hannah Davis", "Ian Martin", "Jasmine Taylor", "Kayden Adams", "Lily Lewis",
    "Mason Young", "Nora Carter", "Oliver Foster", "Penelope Mitchell", "Quinn Parker", "Ruby Turner", "Samuel Baker", "Trinity Robinson", "Violet Turner", "Wesley White",
    "Xavier Davis", "Zoey Smith", "Ava Jackson", "Benjamin Lopez", "Chloe Perez", "David King", "Emma Smith", "Finn Davis", "Grace Wilson", "Henry Anderson", "Isabella White",
    "Jack Harris", "Kayla Martin", "Liam Taylor", "Mia Thompson", "Noah Robinson", "Olivia Turner", "Parker Brown", "Quinn Garcia", "Riley Hall", "Sophia Jackson", "Tyler Lewis",
    "Victoria Martinez", "Wyatt Adams", "Xander Foster", "Yasmine Baker", "Zoe Clark", "Ava Davis", "Benjamin Hall", "Caleb Johnson", "Daisy Lopez", "Elijah Moore", "Faith Parker",
    "Gabriel Turner", "Hannah Baker", "Ian Carter", "Jasmine Davis", "Kayden Foster", "Lily Garcia", "Mason Harris", "Nora Jackson", "Oliver King", "Penelope Lewis", "Quinn Martin",
    "Ruby Martinez", "Samuel Perez", "Trinity Robinson", "Violet Scott", "Wesley Taylor", "Xavier Turner", "Zoey White", "Ava Adams", "Benjamin Clark", "Chloe Davis", "David Foster",
    "Emma Garcia", "Finn Hall", "Grace Jackson", "Henry Lopez", "Isabella Moore", "Jack Parker", "Kayla Smith", "Liam Turner", "Mia Wilson", "Noah Anderson", "Olivia Foster", "Parker Harris",
    "Quinn Johnson", "Riley King", "Sophia Lewis", "Tyler Martin", "Victoria Perez", "William Robinson", "Xander Scott", "Yasmine Taylor", "Zoe Turner", "Ava White", "Benjamin Adams",
    "Caleb Baker", "Daisy Clark", "Elijah Davis", "Faith Foster", "Gabriel Garcia", "Hannah Hall", "Ian Jackson", "Jasmine Lewis", "Kayden Martin", "Lily Moore", "Mason Parker", "Nora Smith",
    "Oliver Turner", "Penelope Wilson", "Quinn Anderson", "Ruby Carter", "Samuel Foster", "Trinity Garcia", "Violet Harris", "Wesley Johnson", "Xavier King", "Zoey Lopez", "Ava Martin",
    "Benjamin Perez", "Chloe Robinson", "David Smith", "Emma Taylor", "Finn Turner", "Grace White", "Henry Adams", "Isabella Baker", "Jack Clark", "Kayla Davis", "Liam Foster", "Mia Garcia",
    "Noah Hall", "Olivia Jackson", "Parker Lewis", "Quinn Martin", "Riley Moore", "Sophia Parker", "Tyler Robinson", "Victoria Turner", "William Wilson", "Xander Adams", "Yasmine Carter", "Zoe Davis",
    "Ava Foster", "Benjamin Garcia", "Caleb Hall", "Daisy Jackson", "Elijah King", "Faith Lopez", "Gabriel Martin", "Hannah Perez", "Ian Robinson", "Jasmine Smith", "Kayden Taylor", "Lily Turner",
    "Mason White", "Nora Adams", "Oliver Baker", "Penelope Clark", "Quinn Foster", "Ruby Garcia", "Samuel Hall", "Trinity Jackson", "Violet Lewis", "Wesley Martin", "Xavier Perez", "Zoey Robinson",
    "Ava Turner", "Benjamin Wilson", "Chloe Adams", "David Carter", "Emma Davis", "Finn Foster", "Grace Garcia", "Henry Hall", "Isabella Jackson", "Jack King", "Kayla Lopez", "Liam Martin",
    "Mia Parker", "Noah Robinson", "Olivia Smith", "Parker Taylor", "Quinn White", "Riley Adams", "Sophia Baker", "Tyler Clark", "Victoria Foster", "William Garcia", "Xander Hall", "Yasmine Jackson",
    "Zoe King", "Ava Lopez", "Benjamin Martin", "Caleb Perez", "Daisy Robinson", "Elijah Smith", "Faith Taylor", "Gabriel White", "Hannah Adams", "Ian Baker", "Jasmine Carter", "Kayden Davis", "Lily Foster",
    "Mason Garcia", "Nora Hall", "Oliver Jackson", "Penelope King", "Quinn Lopez", "Ruby Martin", "Samuel Parker", "Trinity Smith", "Violet Taylor", "Wesley White", "Xavier Adams", "Zoey Baker",
    "Ava Clark", "Benjamin Davis", "Chloe Foster", "David Garcia", "Emma Hall", "Finn Jackson", "Grace King", "Henry Lopez", "Isabella Martin", "Jack Perez", "Kayla Robinson", "Liam Smith", "Mia Taylor",
    "Noah Adams", "Olivia Baker", "Parker Carter", "Quinn Davis", "Riley Foster", "Sophia Garcia", "Tyler Hall", "Victoria Jackson", "William King", "Xander Lopez", "Yasmine Martin", "Zoe Perez", "Ava Robinson",
    "Benjamin Smith", "Caleb Turner", "Daisy Harris", "Elijah Wilson", "Faith Thompson", "Gabriel Green", "Hannah Davis", "Ian Martin", "Jasmine Taylor", "Kayden Adams", "Lily Lewis", "Mason Young", "Nora Carter",
    ]
additional_names = [
    "Aarav Patel", "Aisha Khan", "Akshay Sharma", "Amir Khan", "Anaya Ahmed", "Arjun Reddy", "Ayesha Ali", "Chetan Kumar", "Disha Singh", "Farhan Siddiqui",
    "Gaurav Gupta", "Hadiya Malik", "Ishaan Verma", "Javed Khan", "Juhi Kapoor", "Kabir Kapoor", "Kajal Gupta", "Karthik Sharma", "Lavanya Yadav", "Mehak Rana",
    "Nikhil Kumar", "Noor Ahmed", "Pooja Patel", "Rahul Yadav", "Rehan Khan", "Riya Sharma", "Saif Malik", "Sanya Gupta", "Shahid Ali", "Shreya Singh",
    "Siddharth Verma", "Suman Reddy", "Tanya Patel", "Vikram Singh", "Zain Khan", "Zoya Khan", "Aaryan Ahmed", "Amina Ali", "Arun Reddy", "Bushra Malik",
    "Chirag Gupta", "Diya Khan", "Faisal Ahmed", "Gitanjali Sharma", "Hamza Khan", "Ishita Kapoor", "Kamal Kumar", "Kiran Patel", "Lara Ahmed", "Manoj Verma",
    "Neha Singh", "Osman Khan", "Prachi Gupta", "Ravi Kumar", "Saba Khan", "Sakshi Yadav", "Samarth Sharma", "Shazia Ali", "Shivani Singh", "Sultan Ahmed",
    "Tanvi Patel", "Umar Khan", "Veer Kapoor", "Yasmin Khan", "Zara Khan", "Aadil Malik", "Alia Ahmed", "Ashish Gupta", "Bilal Khan", "Charulata Sharma",
    "Devika Reddy", "Firoz Ahmed", "Gulzar Khan", "Heena Kapoor", "Iqbal Ali", "Kalyani Yadav", "Karan Sharma", "Lakshmi Patel", "Maya Singh", "Nadeem Khan",
    "Parul Gupta", "Rahat Malik", "Rashi Singh", "Sajid Ahmed", "Sana Ali", "Shiva Verma", "Shubhra Patel", "Surya Reddy", "Tariq Khan", "Vandana Sharma",
    "Varun Kapoor", "Zeenat Khan", "Aaliyah Ahmed", "Ali Khan", "Anjali Verma", "Aryan Patel", "Bhavana Gupta", "Danish Khan", "Ekta Yadav", "Fahim Malik",
    "Gautam Sharma", "Hina Kapoor", "Imran Ali", "Kriti Singh", "Krishna Reddy", "Mansi Patel", "Mohammed Khan", "Naina Gupta", "Nishant Sharma", "Prerna Verma",
    "Rahim Ahmed", "Rashmi Singh", "Rishi Kapoor", "Sadia Khan", "Salman Ahmed", "Seema Yadav", "Suresh Verma", "Tasneem Ali", "Tina Patel", "Ujjwal Gupta",
    "Varsha Sharma", "Vishal Yadav", "Yash Kapoor", "Zainab Malik", "Zoya Sharma"]

combined_names = names + additional_names

locations = [
    "New York City", "Los Angeles", "Chicago", "Houston", "Philadelphia", "Phoenix", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Indianapolis", "San Francisco", "Columbus", "Fort Worth", "Charlotte", "Detroit", "El Paso", "Memphis",
    "Boston", "Seattle", "Denver", "Washington, D.C.", "Nashville", "Baltimore", "Oklahoma City", "Louisville", "Portland", "Las Vegas",
    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Long Beach", "Kansas City", "Mesa", "Atlanta", "Virginia Beach",
    "Omaha", "Raleigh", "Miami", "Cleveland", "Tampa", "Pittsburgh", "Oakland", "Minneapolis", "Wichita", "Arlington", "Bakersfield",
    "New Orleans", "Honolulu", "Anaheim", "Tulsa", "Aurora", "Santa Ana", "St. Louis", "Riverside", "Corpus Christi", "Lexington",
    "Stockton", "Pittsburgh", "Cincinnati", "Saint Paul", "Toledo", "Greensboro", "Newark", "Plano", "Henderson", "Lincoln", "Buffalo",
    "Fort Wayne", "Jersey City", "Chula Vista", "Orlando", "St. Petersburg", "Norfolk", "Chandler", "Laredo", "Madison", "Durham",
    "Lubbock", "Irvine", "Winston-Salem", "Glendale", "Garland", "Hialeah", "Reno", "Baton Rouge", "Irvine", "Akron", "Irving", "Fremont"
    ]


organizations = [
    "ABC Inc.", "XYZ Corporation", "Tech Solutions", "InnoTech Industries", "Global Enterprises", "Data Systems Ltd.", "Tech Innovators", "EcoSolutions", "NexaCorp", "Unified Networks",
    "Infinite Technologies", "BlueSky Solutions", "Quantum Systems", "Dynamic Innovations", "Web Wizards", "Synergy Systems", "Tech Titans", "InnoSys Inc.", "FutureTech Solutions", "Acme Industries",
    "Fusion Innovations", "Intellectix", "Advanced IT Services", "Strategic Innovations", "CyberSolutions", "InnoWave Inc.", "InfoTechX", "NexaWave", "TechMasters", "Futuris Tech",
    "InnoSys Corp.", "WebCrafters", "InnoCom Solutions", "NexaTech Innovations", "Data Fusion Technologies", "TechFusion Inc.", "Quantum Innovations", "GlobalWeb Systems", "AceTech Solutions", "WebXpress",
    "Innovative Systems", "TechQuest Inc.", "InnoMind Solutions", "InfoNexa Inc.", "DataPulse Technologies", "InnoLink Corp.", "WebConnectX", "CyberNexa Solutions", "TechNest Innovations", "WebSavvy Inc.",
    "InnoNetX", "InfoMatrix", "Quantum Dynamics", "WebVelocity", "TechCraft Innovations", "NexaCore Solutions", "InnoVision Inc.", "DataBridge Technologies", "TechPulse Innovations", "Stratix Systems",
    "CyberWave Solutions", "WebMasters Inc.", "InnoMinds Corp.", "InfoFusion Technologies", "WebNest Innovations", "QuantumSynergy", "TechWave Inc.", "InnoLogic Solutions", "DataXpress", "WebMatrix Corp.",
    "CyberLink Systems", "InnoWorks Inc.", "InfoCrafters", "TechMind Innovations", "WebMindX", "DataQuest Technologies", "NexaWeb Systems", "InnoFusion Inc.", "TechLogic Solutions", "WebNexa Innovations",
    "QuantumTechX", "Stratix Innovations", "CyberMind Solutions", "WebInno Corp.", "InnoSolutions Inc.", "InfoWeb Systems", "TechSynergy", "InnoNet Innovations", "DataXcel Corp.", "WebQuest Solutions",
    "NexaTechX", "InnoMatrix Technologies", "TechFusion Corp.", "DataWave Innovations", "WebLogic Systems", "CyberCraft Inc.", "QuantumSavvy", "InfoNexa Innovations", "InnoWeb Corp.", "TechConnectX",
    "DataMaster Solutions", "WebCore Innovations", "CyberMinds Inc.", "InnoWebX", "TechSavvy Innovations", "InfoCraft Corp.", "DataSynergyX", "WebLink Solutions", "InnoWave Technologies", "QuantumMind Systems"
    ]

# Initialize the PIIMasker
masker = PIIMasker()

# Set fake names, organizations, and locations
masker.set_fake_names(combined_names)
masker.set_fake_orgs(organizations)
masker.set_fake_locations(locations)

# Input text
input_text = """Your text here with potential PII like names, phone numbers (123-456-7890), 
                    dates of birth (01/01/1980), credit card numbers (1234 5678 9012 3456), 
                    and SSNs (123-45-6789)."""

@app.post("/mask/")
async def mask_pii(request: Item):
    try:
        masked_text = masker.mask_all_pii(request.input)
        return {"masked_text": masked_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))