from flask import Flask, render_template, request
from package import my_credit_score

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract user data from the form
        user_data = {
            "average_monthly_revenue": float(request.form["average_monthly_revenue"]),
            "total_amount_in_debt": float(request.form["total_amount_in_debt"]),
            "max_past_due_amount": float(request.form["max_past_due_amount"]),
            "num_overdue_installments": int(request.form["num_overdue_installments"]),
            "total_open_contracts": int(request.form["total_open_contracts"]),
            "max_past_due_days": int(request.form["max_past_due_days"]),
            "months_in_business": int(request.form["months_in_business"]),
            "payment_methods": request.form.getlist("payment_methods"),
            "age": int(request.form["age"]),
            "num_dependants": int(request.form["num_dependants"]),
            "num_credit_inquiries": int(request.form["num_credit_inquiries"]),
            "region_gdp": float(request.form["region_gdp"]),
            "national_average_gdp": float(request.form["national_average_gdp"]),
            "housing_status": request.form["housing_status"]
        }

        # Calculate credit score and approved loan
        credit_score = my_credit_score.calculate_credit_score(user_data)

                # Get the average_monthly_revenue from user data
        average_monthly_revenue = user_data["average_monthly_revenue"]

        approved_loan = credit_score * (500000 if average_monthly_revenue >= 500000 else average_monthly_revenue)

        
        return render_template("index.html", credit_score=credit_score, approved_loan=approved_loan)

    return render_template("index.html", credit_score=None, approved_loan=None)

if __name__ == "__main__":
    app.run(debug=True)
