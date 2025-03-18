# views.py
import os
import pickle
import numpy as np
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from . models import Usertable,PCOSPrediction,Expert_details




# Load the trained model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'pcod_finder', 'mlmodels', 'rf_classifier.pkl')
with open(MODEL_PATH, 'rb') as model_file:
    rf_classifier = pickle.load(model_file)



def print_hello(request):
    return render(request,'home_page.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dateOfBirth')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        role=0

        # Check if the email already exists
        if Usertable.objects.filter(email=email).exists():
            messages.error(request, "Email already exists! Please use a different email.")
            return redirect('register_page')  # Redirect to the registration page

        # Create a new user
        usertable_Obj = Usertable(name=name, lname=lname, email=email, phoneno=phone, dob=dob, gender=gender, password=password,usertype=role)
        usertable_Obj.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'user_registration.html')




def predict(request):
    if request.method == 'POST':
        try:
            # Collect input values from the form
            user_id = request.session['user_id']
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
                **input_data, prediction_result=result,userid=user_id
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
            request.session['user_id'] = user.id
            if user.usertype=='0':
                return redirect('userdashboard')
            elif user.usertype=='1':
                return redirect('expert_dashboard')

    return render(request,'login.html')

def learmore(request):
    return render(request,'pcos-healthcare-webpage.html')


def healthcareexpert_reg(request):

    if request.method == 'POST':
        name=request.POST.get('fullName')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')

        specialization=request.POST.get('specialization')
        experience=request.POST.get('experience')
        license=request.POST.get('license')
        qualification=request.POST.get('qualification')

        usertable_Obj = Usertable(name=name,email=email,phoneno=phone,password=password,usertype=1)
        usertable_Obj.save()

        last_inserted_id = usertable_Obj.id

        qualification_obj=Expert_details(userid=last_inserted_id,Specialization=specialization,Experience=experience,Medical_License=license,Educational_Qualifications=qualification)
        qualification_obj.save()

        #confirmPassword=request.POST.get('confirmPassword')
        


       
        return redirect('login')

    return render(request,'expert registration.html')


