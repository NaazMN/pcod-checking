# views.py
import os
import pickle
import numpy as np
from django.shortcuts import render
from django.conf import settings



# Load the trained model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'pcod_finder', 'mlmodels', 'rf_classifier.pkl')
with open(MODEL_PATH, 'rb') as model_file:
    rf_classifier = pickle.load(model_file)



def print_hello(request):
    return render(request,'home_page.html')

def register(request):
    if request.POST:
        name=request.POST.get('firstName')
        lname=request.POST.get('lastName')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('dateOfBirth')
        gender=request.POST.get('gender')
        password=request.POST.get('password')

        usertable_Obj = Usertable(name=name,lname=lname,email=email,phoneno=phone,dob=dob,gender=gender,password=password)
        usertable_Obj.save()
    return render(request,'user_registration.html')


def predict(request):
    if request.method == 'POST':
        try:
            # Collect input values from the form
            input_data = [
                float(request.POST.get('cycle_length', 0)),
                float(request.POST.get('FSH', 0)),
                float(request.POST.get('LH', 0)),
                float(request.POST.get('FSH_LH', 0)),
                float(request.POST.get('waist_hip_ratio', 0)),
                float(request.POST.get('TSH', 0)),
                float(request.POST.get('AMH', 0)),
                float(request.POST.get('Vit_D3', 0)),
                float(request.POST.get('PRG', 0)),
                float(request.POST.get('RBS', 0)),
                int(request.POST.get('weight_gain', 0)),
                int(request.POST.get('hair_growth', 0)),
                int(request.POST.get('skin_darkening', 0)),
                int(request.POST.get('hair_loss', 0)),
                int(request.POST.get('pimples', 0)),
                int(request.POST.get('follicle_L', 0)),
                int(request.POST.get('follicle_R', 0)),
                float(request.POST.get('avg_f_size_L', 0)),
                float(request.POST.get('avg_f_size_R', 0))
            ]
            
            # Convert input data into a NumPy array and reshape for prediction
            input_array = np.array(input_data).reshape(1, -1)
            prediction = rf_classifier.predict(input_array)[0]
            result = 'PCOS Detected' if prediction == 1 else 'No PCOS'
            
            return render(request, 'prediction.html', {'prediction': result})
        except Exception as e:
            return render(request, 'prediction.html', {'error': str(e)})
    
    return render(request, 'prediction.html')
def login(request):
    return render(request,'login.html')
