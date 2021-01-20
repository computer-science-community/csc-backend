import models
import app

app.db.create_all()
competitive_coding = models.Pillar(
    name="Competitive Coding", email="csambassador@cs.rit.edu")
mentoring = models.Pillar(name="Mentoring", email="csambassador@cs.rit.edu")
social = models.Pillar(name="Social", email="csambassador@cs.rit.edu")
app.db.session.add(competitive_coding)
app.db.session.add(mentoring)
app.db.session.add(social)
app.db.session.commit()

print(app.db.session.query(models.Pillar).all())
