import model, stream

model.Factory.create(User, 10)
model.session.commit()
