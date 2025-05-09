import google.genai as genai

import tkinter as tk
import tkinter.messagebox as messagebox
from fpdf import FPDF
import os


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
api_key = os.environ.get('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

model_name = "gemini-1.5-flash-latest"

 # Create gemini client
client = genai.Client(api_key=api_key)

address = ""
condition = ""
size = ""
year_Built = ""
budget = ""
design = ""



# actual code 
def generate_summary():
    
    address = address_input.get("1.0", tk.END).strip()
    condition = condition_input.get("1.0", tk.END).strip()
    size = size_input.get("1.0", tk.END).strip()
    year_Built = year_input.get("1.0", tk.END).strip()
    budget = budget_input.get("1.0", tk.END).strip()
    design = design_input.get("1.0", tk.END).strip()
    

    # Send prompt
    prompt = f"""Generate a detailed analysis for the comprehensive remodeling/renovation of the address provided.The analysis should begin with the subject of the remodeling and clearly state the home address and the desired design aesthetic (e.g., 'Modern Farmhouse Renovation at [Address]').


Incorporate an analysis of the property based on the following fixed criteria:


Address: {address}
Condition of the home: {condition} 
Size of home:  {size}
Year the home was built: {year_Built}
Budget in dollars : {budget}
Desired renovation upgrades: {design}
As part of the analysis, you must: 


1.  Develop a phased plan of action with estimated potential costs for each major phase and sub-task. The phases should be logically sequenced (e.g., Demolition & Structural Repairs, Utilities Upgrade, Interior Finishes, Exterior Improvements). Within each phase, break down specific tasks and provide a potential cost range based on the specified location, condition, size, and desired design. For example:
    * **Phase 1: Demolition & Structural Repairs**
        * Demolition and debris removal: $[Range]
        * Foundation repair (if needed): $[Range]
        * Roof repair/replacement: $[Range]
        * Framing repairs/modifications: $[Range]
    * **Phase 2: Utilities Upgrade**
        * Electrical rewiring and new panel: $[Range]
        * Plumbing system overhaul: $[Range]
        * HVAC system replacement: $[Range]
    * **Phase 3: Interior Finishes**
        * Flooring installation (specify type and cost per sqft): $[Range]
        * Wall and ceiling work (drywall, painting): $[Range]
        * Kitchen renovation (cabinets, countertops, appliances): $[Range]
        * Bathroom renovations (fixtures, tiling, vanities): $[Range]
        * Lighting fixtures: $[Range]
    * **Phase 4: Exterior Improvements**
        * Siding repair/replacement: $[Range]
        * Window and door replacement: $[Range]
        * Landscaping: $[Range]
        * Painting: $[Range]
5.  Include a summary of the total estimated cost range and a brief discussion of potential cost overruns and strategies for staying within the provided budget.
6.  Clearly state that these are preliminary estimates and that obtaining detailed quotes from local contractors is essential for accurate budgeting.


The final output should adhere to this structure and including all the requested information, and cost estimates.
"""

  

#actual code 
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=prompt
        )
        print(response.text)
    except:
        messagebox.showerror(
            "Error", "An error occurred while getting data from Google Gemini."
        )
    else:
        gen_label.config(text="Creating PDF ...")
        root.update_idletasks()

    try:
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=13)
        pdf.multi_cell(0, 10, txt=response.text)
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        pdf.output(os.path.join(downloads_folder, f"{address}project summary.pdf"))
    except:
        messagebox.showerror("Error", "An error occurred while creating your PDF.")
    else:
        gen_label.config(text="Done! Check your Downloads.")
        root.update_idletasks()





#actual code 
root = tk.Tk()
root.title(" KSM Renovation planner")
root.geometry("725x1000")
root.configure(bg="#0048FF") 

# style = {"relief": "solid", "bd": 2, "highlightbackground": "white", "highlightthickness": 1}
title_label = tk.Label(root, text="K&M Home Renovation Planner", font=("Arial", 30), bg="#0048FF", fg="white", )
title_label.pack(pady=5)
description_label = tk.Label(root, text="""input the following fields to see how much your home renovation project will cost 
 including a pdf generation of your project summary""", bg="#0048FF", fg="white", font=("Arial", 15) )
description_label.pack(pady=5)
address_label = tk.Label(root, text=" property address:", bg="#0048FF", fg="white", font=("Arial", 15) )
address_label.pack(pady=5)
address_input = tk.Text(root, height=2, width=60, )
address_input.pack(pady=5)

condition_label = tk.Label(root, text=" The current condition of your home?:", bg="#0048FF", fg="white", font=("Arial", 15) )
condition_label.pack(pady=5)
condition_input = tk.Text(root, height=3, width=60,)
condition_input.pack(pady=5)

size_label = tk.Label(root, text="property size:", bg="#0048FF", fg="white", font=("Arial", 15))
size_label.pack(pady=5)
size_input = tk.Text(root, height=3, width=60, )
size_input.pack(pady=5)

year_label = tk.Label(root, text="year the home was built:", bg="#0048FF", fg="white", font=("Arial", 15) )
year_label.pack(pady=5)
year_input = tk.Text(root, height=2, width=60, )
year_input.pack(pady=5)

budget_label = tk.Label(root, text=" your intended budget:", bg="#0048FF", fg="white", font=("Arial", 15) )
budget_label.pack(pady=5)
budget_input = tk.Text(root, height=2, width=60, )
budget_input.pack(pady=5)

design_label = tk.Label(root, text=" what are the ideal changes you want to make to your home?:", bg="#0048FF", fg="white", font=("Arial", 15) )
design_label.pack(pady=5)
design_input = tk.Text(root, height=10, width=60, )
design_input.pack(pady=5)


def update_label():
    gen_label.config(text="Generating...")
    gen_label.update()
    root.update_idletasks()


gen_label = tk.Label(root, text="Click to generate!", bg="#0048FF", fg="white", font=("Arial", 20) )
gen_label.pack()

gen_button = tk.Button(
    root, text="Generate", width=30, command=lambda: [update_label(), generate_summary()], bg="red", fg="white", font=("Arial", 12), 
)
gen_button.pack()



root.mainloop()
