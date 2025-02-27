# views.py
import os
import pickle
import numpy as np
from django.shortcuts import render,redirect
from django.conf import settings
from . models import Usertable,PCOSPrediction




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
            input_data = {
                'cycle_length': float(request.POST.get('cycle_length', 0)),
                'FSH': float(request.POST.get('FSH', 0)),
                'LH': float(request.POST.get('LH', 0)),
                'FSH_LH': float(request.POST.get('FSH_LH', 0)),
                'waist_hip_ratio': float(request.POST.get('waist_hip_ratio', 0)),
                'TSH': float(request.POST.get('TSH', 0)),
                'AMH': float(request.POST.get('AMH', 0)),
                'Vit_D3': float(request.POST.get('Vit_D3', 0)),
                'PRG': float(request.POST.get('PRG', 0)),
                'RBS': float(request.POST.get('RBS', 0)),
                'weight_gain': int(request.POST.get('weight_gain', 0)),
                'hair_growth': int(request.POST.get('hair_growth', 0)),
                'skin_darkening': int(request.POST.get('skin_darkening', 0)),
                'hair_loss': int(request.POST.get('hair_loss', 0)),
                'pimples': int(request.POST.get('pimples', 0)),
                'follicle_L': int(request.POST.get('follicle_L', 0)),
                'follicle_R': int(request.POST.get('follicle_R', 0)),
                'avg_f_size_L': float(request.POST.get('avg_f_size_L', 0)),
                'avg_f_size_R': float(request.POST.get('avg_f_size_R', 0)),
            }

            # Convert input data into a NumPy array and reshape for prediction
            input_array = np.array(list(input_data.values())).reshape(1, -1)
            prediction = rf_classifier.predict(input_array)[0]
            result = 'PCOS Detected' if prediction == 1 else 'No PCOS'
            
            # Save data in the database
            pcos_entry = PCOSPrediction.objects.create(
                **input_data, prediction_result=result
            )
            pcos_entry.save()
            last_entry = PCOSPrediction.objects.latest('id')  
            # Pass data to the template
            return render(request, 'pcos_res_print.html', {'prediction': last_entry})

        except Exception as e:
            return render(request, 'prediction.html', {'error': str(e)})
    
    return render(request, 'prediction.html')



def login(request):
    
    if request.method == 'POST':
        uname=request.POST.get('email')
        pass_t=request.POST.get('password')
        user=Usertable.objects.get(email=uname)
        if user.password==pass_t:
            return redirect('userdashboard')
    return render(request,'login.html')

def learmore(request):
    return render(request,'pcos-healthcare-webpage.html')


