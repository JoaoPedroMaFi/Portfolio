from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib

SKILLS = {
    "C#": 90,
    "Python": 90,
    "MySQL": 70,
    "API/SOAP": 60,
}
EXPERIENCE = {
    "2012 - 2022": ["Operador de corte têxtil", "Farsilcortex", "Barcelos", "Corte de peças a feitio"],
}
EDUCATION = {
    "2019 - 2022": ["Licenciatura em Engenhraria. de Sistemas Informáticos", "Portugal", "Barcelos"],
    "2008 - 2011": ["Curso Científico-Humanístico de Ciências e Tecnologias", "Portugal", "Barcelos"],
}
app = Flask(__name__)
Bootstrap5(app)


@app.route('/')
def home():
    return render_template("index1.html",
                           SKILLS=SKILLS,
                           EXPERIENCE=EXPERIENCE,
                           EDUCATION=EDUCATION)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    my_email = "your email"
    password = "password"
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('comment')

        # Sending email
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="to address",
                msg=f"Subject: Contact from User\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Subject: {subject}\n"
                    f"Message: {message}"
            )

    return render_template("index1.html",
                           SKILLS=SKILLS,
                           EXPERIENCE=EXPERIENCE,
                           EDUCATION=EDUCATION)


if __name__ == "__main__":
    app.run(debug=True)
