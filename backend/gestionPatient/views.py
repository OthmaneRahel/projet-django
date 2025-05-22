# modules imports :
import pprint
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
import json
# Models import :
from .models import Patient,Medecin,RendezVous,Secretaire,Demande,Facture,Archive,Messages_secretaire_medecin,RapportMedicalPatient,Administrateur,Messages_admin_medecin,Messages_admin_secretaire

class Home(View):
    def get(self,request):
        return render(request,'interfacePatient/homePage.html')
class LoginPage(View):
    def get(self,request):
        return render(request,'loginInterface/loginPage.html')
    def post(self,request):
        userEmail = request.POST.get('email')
        userPassword = request.POST.get('password')
        userconnecte = authenticate(username=userEmail,password=userPassword)
        if userconnecte is not None:
            login(request, userconnecte)
            #login patient
            if userconnecte.email.endswith("@gmail.com"):
                return redirect("home")
            #login medecin
            elif userconnecte.email.endswith("@medecin.com"):
                nombrePatient = Patient.objects.count()
                nombreRendezVous = RendezVous.objects.filter(medecin_id = userconnecte.id).count()
                rendezVousEnCours = RendezVous.objects.filter(statut="En Cours").count()
                rendezVousValide = RendezVous.objects.filter(statut="Confirmé").count()
                rendezVousRecents = RendezVous.objects.raw("SELECT p.image,r.* FROM gestionpatient_rendezvous r JOIN gestionpatient_patient p ON p.id = r.patient_id WHERE r.medecin_id = %s",[userconnecte.id])
                rendezrousrecents = list(rendezVousRecents)[:5]
                rendezVous = RendezVous.objects.filter(medecin_id=request.user.id)
                rendezVous_json = serialize('json', rendezVous)
                rendezVousAujourdhui = RendezVous.objects.filter(dateRendezVous=date.today()).count()
                return render(request,'interfaceMedecin/homePageMedecin.html', {"rendezVous_json":rendezVous_json,"nombrePatient":nombrePatient,"nombreRendezVous":nombreRendezVous,"rendezVousRecents":rendezrousrecents,"rendezVousEnCours":rendezVousEnCours,"rendezVousValide":rendezVousValide,"rendezVousAujourdhui":rendezVousAujourdhui})
            #login secretaire
            elif userconnecte.email.endswith("@secretaire.com"):
                    rendezVousAujourdhui = RendezVous.objects.filter(dateRendezVous=date.today()).count()
                    return render(request,"interfaceSecretaire/homePage.html",{"rendezVousAujourdhui":rendezVousAujourdhui})
            else:
                return render(request,'interfaceAdmin/homePageAdmin.html')
        else:
            messages.error(request,"Votre Email ou Password est incorrecte,Veuillez ressayer")
            return redirect("loginvalidation")
def register(request):
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    email = request.POST.get('email')
    adresse = request.POST.get('adresse')
    numeroTelephone = request.POST.get('numtel')
    cin = request.POST.get('cin')
    password = request.POST.get('password')
    hashed_password = make_password(password)
    patient = Patient.objects.create(
        nom=nom,
        prenom=prenom,
        email=email,
        adresse=adresse,
        numeroTelephone=numeroTelephone,
        cin=cin,
        password=hashed_password,
        image= "https://urls.fr/Q2tGOp"
    )
    messages.success(request,"Compte crée avec success")
    return redirect("loginvalidation")
def ListMedecin(request):
    listMedecin = Medecin.objects.all();
    return render(request,"interfacePatient/listMedecin.html",{"medecins":listMedecin})
def detailMedecin(request,medecin_id):
    medecin = Medecin.objects.get(id=medecin_id)
    return render(request,"interfacePatient/DetailMedecin.html",{"medecin":medecin})
class FormPage(View):
    def get(self,request,patient_id,medecin_id):
        medecin = Medecin.objects.get(id=medecin_id)
        return render(request,'interfacePatient/formPage.html',{"medecin":medecin,"patient_id":patient_id,"medecin_id":medecin_id})
def saveRendezVous(request):
    patientid = request.POST.get('patient_id')
    medecin_id = request.POST.get('medecin_id')
    titreRend = request.POST.get('titreRendezVous')
    dateRendezVous = request.POST.get('dateRendezVous')
    typeRendezVous = request.POST.get('typeRendezVous')
    descriptionRendezVous = request.POST.get('descriptionRendezVous')
    rendezVous = RendezVous.objects.create(
        titreRendezVous = titreRend,
        typeRendezVous = typeRendezVous,
        dateRendezVous = dateRendezVous,
        descriptionRendezVous = descriptionRendezVous,
        patient_id = patientid,
        medecin_id = medecin_id
    )
    return redirect('home')

class HomePageMedecin(View):
    def get(self,request):
        nombreRendezVous = RendezVous.objects.filter(medecin_id = request.user.id).count()
        rendezVousEnCours = RendezVous.objects.filter(statut="En Cours",medecin_id=request.user.id).count()
        rendezVousValide = RendezVous.objects.filter(statut="Confirmé",medecin_id=request.user.id).count()
        rendezVousRecents = RendezVous.objects.filter(medecin_id=request.user.id)[:4]
        rendezVous = RendezVous.objects.filter(medecin_id=request.user.id)
        rendezVousAujourdhui = RendezVous.objects.filter(dateRendezVous=date.today(),medecin_id = request.user.id).count()
        events = []
        for rdv in rendezVous:
            events.append({
                "title": rdv.titreRendezVous,
                "start": rdv.dateRendezVous.isoformat(),
                "end": rdv.dateRendezVous.isoformat()
            })
        rendezVous_json = json.dumps(events)
        return render(request,"interfaceMedecin/homePageMedecin.html",{"rendezVous_json":rendezVous_json,"nombreRendezVous":nombreRendezVous,"rendezVousRecents":rendezVousRecents,"rendezVousEnCours":rendezVousEnCours,"rendezVousValide":rendezVousValide,"rendezVousAujourdhui":rendezVousAujourdhui})
class FormRegister(View):
    def get(self,request):
        return render(request,"interfaceMedecin/registerMedecin.html")
    def post(self,request):
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        numeroTelephone = request.POST.get('numeroTelephone')
        profession = request.POST.get('profession')
        cin = request.POST.get('cin')
        descriptionMedecin = request.POST.get('descriptionMedecin')
        salaire = request.POST.get('salaire')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        adresse = request.POST.get('adresse')
        prix_consultation = request.POST.get('prix_consultation')
        if password == confirmpassword :
            password_hash=make_password(password)
            medecin = Medecin.objects.create(
                nom = nom,
                prenom = prenom,
                email = email,
                numeroTelephone = numeroTelephone,
                profession = profession,
                cin = cin,
                descriptionMedecin = descriptionMedecin,
                salaire = salaire,
                password = password_hash,
                adresse = adresse,
                prix_consultation = prix_consultation,
                image= "https://urls.fr/Q2tGOp"
            )
            messages.success(request,"Medecin ajouté avec success")
            return redirect('listeMedecinAdmin')
        else:
            return render(request,"interfaceMedecin/registerMedecin.html",{"message":"Veuillez Entrer le meme code "})
def logout_user(request):
        logout(request)
        return redirect("loginvalidation")
def listRendezVous(request):
    rendezVous = RendezVous.objects.filter(medecin_id = request.user.id)
    return render(request,"interfaceMedecin/listRendezVous.html",{"rendezVous":rendezVous})
def listPatient(request):
    patients = Patient.objects.raw("SELECT distinct p.*,r.* FROM gestionpatient_patient p JOIN gestionpatient_rendezvous r on r.patient_id = p.id WHERE r.medecin_id = %s",[request.user.id])
    return render(request,"interfaceMedecin/listPatient.html",{"patients":patients})
def detailPatient(request,patient_id):
    patient = Patient.objects.get(id=patient_id);
    consultations = RapportMedicalPatient.objects.filter(patient_id=patient_id)
    return render(request,"interfaceMedecin/detailPatient.html",{"patient":patient,"consultations":consultations})
def profileMedecin(request,id):
    medecin = Medecin.objects.get(id=id)
    return render(request,"interfaceMedecin/profileMedecin.html",{"medecin":medecin})
def detailRendezVous(request,id):
    rendezvous = RendezVous.objects.get(id=id)
    return render(request,"interfaceMedecin/detailRendezVous.html",{"rendezvous":rendezvous})
def envoyerEmail(request):
    message = (
        f"Merci pour votre Rendez !\n\n"
            f"Montant total:  DT\n"
    )
    print(f"Email à envoyer : ")
    send_mail(
        subject="Votre emprunte de livres",
        message= message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=3,
        fail_silently=False,
    )
    # Message To Secretaire :
class EnvoyerMessageAuSecretaire(View):
    def get(self,request):
        listeSecretaire = Secretaire.objects.all();
        return render(request,"interfaceMedecin/interfaceChat.html",{"listeSecretaire":listeSecretaire})
    def post(self,request):
        message = request.POST.get("message")
        secretaire_id = request.POST.get("secretaire_id")
        destination = request.POST.get("destination")
        Messages_secretaire_medecin.objects.create(
            secretaire_id=secretaire_id,
            message=message,
            source = request.user.nom,
            destination = destination,
            medecin_id=request.user.id
        )
        return redirect(f"/secretaire/messages/{secretaire_id}")
def messageMedecinAuSecretaire(request,secretaire_id):
    listeSecretaire = Secretaire.objects.all()
    secretaire = Secretaire.objects.get(id=secretaire_id)
    secretaireMessages = Messages_secretaire_medecin.objects.filter(secretaire_id=secretaire_id,medecin_id=request.user.id)
    return render(request,"interfaceMedecin/interfaceChat.html",{"secretaireMessages":secretaireMessages,"secretaire_actif":secretaire,"listeSecretaire":listeSecretaire})
def FormPageSecretaire(request):
    rendezVousAujourdhui = RendezVous.objects.filter(dateRendezVous=date.today()).count()
    rendezVous = RendezVous.objects.all()
    nombreRendezVous = rendezVous.count()
    nombreMessageNolu = Messages_secretaire_medecin.objects.filter(vu=False).count()
    events = []
    for rdv in rendezVous:
        events.append({
            "title": rdv.titreRendezVous,
            "start": rdv.dateRendezVous.isoformat(),
            "end": rdv.dateRendezVous.isoformat()
        })
    rendezVous_json = json.dumps(events)
    return render(request,"interfaceSecretaire/homePage.html",{"nombreRendezVous":nombreRendezVous,"rendezVous_json":rendezVous_json,"rendezVousAujourdhui":rendezVousAujourdhui,"nombreMessageNolu":nombreMessageNolu})
class FormRegisterSecretaire(View):
    def get(self,request):
        return render(request,"interfaceSecretaire/registerSecretaire.html")
    def post(self,request):
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        numeroTelephone = request.POST.get('numeroTelephone')
        cin = request.POST.get('cin')
        salaire = request.POST.get('password')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        adresse = request.POST.get('adresse')
        if password == confirmpassword :
            password_hash=make_password(password)
            secretaire = Secretaire.objects.create(
                nom = nom,
                prenom = prenom,
                email = email,
                numeroTelephone = numeroTelephone,
                cin = cin,
                salaire=salaire,
                password = password_hash,
                adresse = adresse,
                image= "https://urls.fr/Q2tGOp"
            )
            return redirect('listesecretaire')
        else:
            return render(request,"interface",{"message":"Veuillez Entrer le meme code "})
        
def listeRendez(request):
    rendezvous = RendezVous.objects.all()
    return render(request,"interfaceSecretaire/listeRendezVous.html",{"rendezvous":rendezvous})

def validerRendezVous(request,rendezVous_id):
    rendezvous = RendezVous.objects.get(id=rendezVous_id)
    rendezvous.statut = "Confirmé"
    rendezvous.save()
    messages.success(request,"le Rendez-vous est validé avec success")
    return redirect("rendezVous")

def archiverRendezVous(request,rendezVous_id):
    rendezvous = RendezVous.objects.get(id=rendezVous_id)
    Archive.objects.create(
        titreRendezVous=rendezvous.titreRendezVous,
        typeRendezVous=rendezvous.typeRendezVous,
        dateRendezVous=rendezvous.dateRendezVous,
        descriptionRendezVous=rendezvous.descriptionRendezVous,
        statut="Archivé",
        patient_id=rendezvous.patient_id,
        medecin_id=rendezvous.medecin_id
    )
    rendezvous.delete()
    messages.success(request,"Rendez-vous archivé")
    return redirect("rendezVous")

#Message Entre Secretaire et le Medecin (L'envoi de message de Secretaire au Medecin)
class EnvoyerMessageAuMedecin(View):
    def get(self,request):
        listMedecin = Medecin.objects.all();
        return render(request,"interfaceSecretaire/chat_medecin_secretaire.html",{"medecins":listMedecin})
    def post(self,request):
        message = request.POST.get("message")
        medecin_id = request.POST.get("medecin_id")
        destination = request.POST.get("destination")
        Messages_secretaire_medecin.objects.create(
            secretaire_id=request.user.id,
            message=message,
            source = request.user.nom,
            destination = destination,
            medecin_id=medecin_id
        )
        return redirect(f"/messages/{medecin_id}")

def chatavecmedecin(request,medecin_id):
    medecins = Medecin.objects.all()
    medecin = Medecin.objects.get(id=medecin_id);
    messagesMedecin = Messages_secretaire_medecin.objects.filter(medecin_id=medecin.id,secretaire_id=request.user.id)
    return render(request,"interfaceSecretaire/chat_medecin_secretaire.html",{"medecin_actif":medecin,"messages":messagesMedecin,"medecins":medecins})


#detail rendez-vous interface secretaire:
def detailrendezvous(request,id):
    rendezvous = RendezVous.objects.get(id=id)
    return render(request,"interfaceSecretaire/detailRendezVous.html",{"rendezvous":rendezvous})

#envoyer un email comme quoi votre rendez-vous est validé:
def envoyerEmailAuPatient(request):
    message = (
        f"Bonjour,{request.POST.get("nomComplet")}"
        f" Merci pour votre Rendez-vous !\n\n"
            f"Votre Rendez-vous a été bien validé dans la date {request.POST.get("dateRendezVous")} merci de respecter votre horaire \n"
            f" Merci et a bientot"
    )
    send_mail(
        from_email = "noreply@monsite.com",
        subject="Validation de rendez-vous",
        message= message,
        recipient_list=[request.POST.get("mailPatient")],
        fail_silently=False,
    )
    messages.success(request,f"L'email a été bien envoyé a {request.POST.get("mailPatient")}")
    return redirect("rendezVous")

#Marquer le message comme lu :
def MarquerMessageCommeLu(request,message_id):
    medecin_id = request.POST.get("medecin_id")
    secretaire_id = request.POST.get("secretaire_id")
    message = Messages_secretaire_medecin.objects.get(id=message_id)
    message.vu = True;
    message.save()
    if request.user.email.endswith("@secretaire.com"):
        return redirect(f"/messages/{medecin_id}")
    else:
        return redirect(f"/secretaire/messages/{secretaire_id}")

#ajouter un rapport medical pour un patient affectee a lui :
class RapportMedical(View):
    def get(self,request,rendezvous_id):
        listRendezvous = RendezVous.objects.get(id=rendezvous_id)
        rdv = RapportMedicalPatient.objects.filter(rendezvous_id=rendezvous_id)
        if rdv.exists():
            messages.error(request,"Consultation deja fait !")
            return redirect("homelistRendezvous")
        else:  
            return render(request,"interfaceMedecin/rapportMedical.html",{"listRendezvous":listRendezvous})
    def post(self,request,rendezvous_id):
        patient_id = request.POST.get("patient_id")
        description = request.POST.get("description")
        prix = request.POST.get("prix")
        RapportMedicalPatient.objects.create(
            patient_id=patient_id,
            description=description,
            prix=prix,
            medecin_id=request.user.id,
            rendezvous_id =rendezvous_id,
        )
        messages.success(request,"Rapport Ajouté !")
        return redirect("homePageMedecin")

#Edit profil pour le medecin :

class EditProfilMedecin(View):
    def get(self,request,user_id):
        medecin = Medecin.objects.get(id=user_id)
        return render(request,"interfaceMedecin/editProfil.html",{"medecin":medecin})
    def post(self,request,user_id):
        image = request.FILES.get('image')
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        numero_telephone = request.POST.get("numeroTelephone")
        profession = request.POST.get("profession")
        # cin = request.POST.get("cin")
        salaire = request.POST.get("salaire")
        prix_consultation = request.POST.get("prix_consultation")
        # email = request.POST.get("email")
        adresse = request.POST.get("adresse")
        medecin = Medecin.objects.get(id=user_id)
        if image is None :
            medecin.image = medecin.image
        else:
            medecin.image = image
        medecin.nom = nom
        medecin.prenom = prenom
        medecin.numeroTelephone = numero_telephone
        medecin.profession = profession
        medecin.salaire = salaire
        medecin.prix_consultation = prix_consultation
        medecin.adresse = adresse
        medecin.save()
        return redirect("homePageMedecin")
    
#edit description medecin :

class EditDescriptionMedecin(View):
    def get(self,request,user_id):
        medecin = Medecin.objects.get(id=user_id)
        return render(request,"interfaceMedecin/editDescription.html",{"medecin":medecin})
    def post(self,request,user_id):
        description = request.POST.get("description")
        medecin = Medecin.objects.get(id=user_id)
        medecin.descriptionMedecin = description
        medecin.save()
        return redirect("homePageMedecin")
    
# get construire facture
def construireFacture(request,rendezvous_id):
    patient_id = request.POST.get("patient_id")
    consultation = RapportMedicalPatient.objects.get(patient_id=patient_id)
    nombreRendezVous = RendezVous.objects.filter(patient_id=patient_id).count()
    totalConsultation = 0;
    if Facture.objects.filter(rendezvous_id=rendezvous_id).exists():
        messages.error(request, "Une facture existe déjà pour ce rendez-vous.")
        return redirect("rendezVous")
    remise = 0
    if nombreRendezVous >= 10:
        remise = 10;
        totalConsultation = consultation.prix * 0.90
        return render(request,"interfaceSecretaire/effectuerFacture.html",{"remise":remise,"totalConsultation":totalConsultation,"consultation":consultation})
    elif nombreRendezVous >= 5 and nombreRendezVous <= 9:
        remise = 5;
        totalConsultation = consultation.prix * 0.95
        return render(request,"interfaceSecretaire/effectuerFacture.html",{"remise":remise,"totalConsultation":totalConsultation,"consultation":consultation})
    else:
        totalConsultation = consultation.prix
        return render(request,"interfaceSecretaire/effectuerFacture.html",{"remise":remise,"totalConsultation":totalConsultation,"consultation":consultation})
    
#sauvegarder facture :
def sauvegarderFacture(request, rendezvous_id):
    Facture.objects.create(
        patient_id=request.POST.get("patient_id"),
        rendezvous_id=rendezvous_id,
        prixFacture=request.POST.get("prixFacture"),
        note_supplementaire=request.POST.get("note_supplementaire")
    )
    messages.success(request, "Facture enregistrée avec succès!")
    return redirect("rendezVous")

#filtrer les secretaires selon le nom
def filtrerSecretaire(request):
    nom = request.POST.get('nom')
    secretaire = Secretaire.objects.filter(nom=nom)
    if secretaire.exists():
        return render(request,"interfaceAdmin/listeSecretaire.html",{"secretaire":secretaire})
    else:
        messages.error(request, "Secretaire avec ce nom n'existe pas !")
        return redirect("listesecretaire")
def filtrerMedecin(request):
    nom = request.POST.get('nom')
    medecin = Medecin.objects.filter(nom=nom)
    if medecin.exists():
        return render(request,"interfaceAdmin/listeMedecin.html",{"medecin":medecin})
    else:
        messages.error(request, "Medecin avec ce nom n'existe pas !")
        return redirect("listeMedecinAdmin")
def filtrerSecretaire(request):
    nom = request.POST.get('nom')
    secretaire = Secretaire.objects.filter(nom=nom)
    if secretaire.exists():
        return render(request,"interfaceAdmin/listeSecretaire.html",{"secretaire":secretaire})
    else:
        messages.error(request, "Secretaire avec ce nom n'existe pas !")
        return redirect("listesecretaire")


def listesecretaire(request):
    listesecretaire = Secretaire.objects.all();
    return render(request,"interfaceAdmin/listeSecretaire.html",{"listesecretaire":listesecretaire})

# detail patient :
def detailPatient(request,patient_id):
    patient = Patient.objects.get(id=patient_id);
    consultations = RapportMedicalPatient.objects.filter(patient_id=patient_id)
    return render(request,"interfaceMedecin/detailPatient.html",{"patient":patient,"consultations":consultations})


class EditProfilPatient(View):
    def get(self,request,patient_id):
        patient = Patient.objects.get(id=patient_id);
        consultations = RapportMedicalPatient.objects.filter(patient_id=patient_id)
        return render(request,"interfacePatient/detailProfil.html",{"patient":patient,"consultations":consultations})
    def post(self,request,patient_id):
        image = request.FILES.get('image')
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        numero_telephone = request.POST.get("numeroTelephone")
        adresse = request.POST.get("adresse")
        patient = Patient.objects.get(id=patient_id)
        patient.nom = nom
        patient.prenom = prenom
        patient.numeroTelephone = numero_telephone
        patient.adresse = adresse
        if image is None :
            patient.image = patient.image
        else:
            patient.image = image
        patient.save()
        return redirect(f"/profil/{patient_id}")
    
#edit profil secretaire
class EditProfilSecretaire(View):
    def get(self,request,secretaire_id):
        secretaire = Secretaire.objects.get(id=secretaire_id);
        return render(request,"interfaceSecretaire/detailProfil.html",{"secretaire":secretaire})
    def post(self,request,secretaire_id):
        image = request.FILES.get('image')
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        numero_telephone = request.POST.get("numeroTelephone")
        adresse = request.POST.get("adresse")
        secretaire = Secretaire.objects.get(id=secretaire_id);
        secretaire.nom = nom
        secretaire.prenom = prenom
        secretaire.numeroTelephone = numero_telephone
        secretaire.adresse = adresse
        if image is None :
            secretaire.image = secretaire.image
        else:
            secretaire.image = image
        secretaire.save()
        return redirect(f"/editProfilSecretaire/{secretaire_id}")
    
# home page admin :
def homePageAdmin(request):
    nombrepatients = Patient.objects.all().count();
    nombrerendezvous = RendezVous.objects.all().count();
    nombresecretaire = Secretaire.objects.all().count();
    nombremedecin = Medecin.objects.all().count();
    rendezVous = RendezVous.objects.all()
    events=[]
    for rdv in rendezVous:
        events.append({
            "title": rdv.titreRendezVous,
            "start": rdv.dateRendezVous.isoformat(),
            "end": rdv.dateRendezVous.isoformat()
        })
    rendezVous_json = json.dumps(events)
    return render(request,"interfaceAdmin/homePageAdmin.html",{"rendezVous_json":rendezVous_json,"nombrepatients":nombrepatients,"nombrerendezvous":nombrerendezvous,"nombresecretaire":nombresecretaire,"nombremedecin":nombremedecin})
# creation compte admin :
class RegisterAdmin(View):
    def get(self,request):
        return render(request,"interfaceAdmin/registerAdmin.html")
    def post(self,request):
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            email = request.POST.get('email')
            numeroTelephone = request.POST.get('numeroTelephone')
            cin = request.POST.get('cin')
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            adresse = request.POST.get('adresse')
            if password == confirmpassword :
                password_hash=make_password(password)
                Administrateur.objects.create(
                    nom = nom,
                    prenom = prenom,
                    email = email,
                    numeroTelephone = numeroTelephone,
                    cin = cin,
                    password = password_hash,
                    adresse = adresse,
                    image= "https://urls.fr/Q2tGOp"
                )
                return redirect('loginpagepatient')
            else:
                return render(request,"interface",{"message":"Veuillez Entrer le meme code "})
#liste de medecin
class ListMedecinAdmin(View):
    def get(self,request):
        listeMedecin = Medecin.objects.all()
        return render(request,"interfaceAdmin/listeMedecin.html",{"listeMedecin":listeMedecin})
#supprimer et voir detail d'un medecin 
def supprimerMedecin(request,medecin_id):
    medecin = Medecin.objects.get(id=medecin_id);
    medecin.delete()
    messages.success(request,"Medecin Supprimé avec success")
    return redirect("listeMedecinAdmin")
def detailMedecinAdmin(request,medecin_id):
    medecin = Medecin.objects.get(id=medecin_id);
    return render(request,"interfaceAdmin/detailMedecin.html",{"medecin":medecin})

#supprimer et voir detail secretaire 
def supprimerSecretaire(request,secretaire_id):
    secretaire = Secretaire.objects.get(id=secretaire_id);
    secretaire.delete()
    messages.success(request,"Secretaire a été bien supprimé")
    return redirect("listesecretaire")
def detailSecretaire(request,secretaire_id):
    secretaire = Secretaire.objects.get(id=secretaire_id);
    return render(request,"interfaceAdmin/detailSecretaire.html",{"secretaire":secretaire})

class EditProfilAdmin(View):
    def get(self,request,user_id):
        admin = Administrateur.objects.get(id=user_id);
        return render(request,"interfaceAdmin/detailProfil.html",{"admin":admin})
    def post(self,request,user_id):
        image = request.FILES.get('image')
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        numero_telephone = request.POST.get("numeroTelephone")
        adresse = request.POST.get("adresse")
        admin = Administrateur.objects.get(id=user_id);
        admin.nom = nom
        admin.prenom = prenom
        admin.numeroTelephone = numero_telephone
        admin.adresse = adresse
        if image is None :
            admin.image = admin.image
        else:
            admin.image = image
        admin.save()
        return redirect(f"/editProfiladmin/{user_id}")


#chat entre l'admin et le medecin :
class ChatEntreAdminMedecin(View):
    def get(self,request):
        listeMedecin = Medecin.objects.all();
        return render(request,"interfaceAdmin/interfaceChatMedecin.html",{"listeMedecin":listeMedecin})
    def post(self,request):
        message = request.POST.get("message")
        medecin_id = request.POST.get("medecin_id")
        destination = request.POST.get("destination")
        Messages_admin_medecin.objects.create(
            medecin_id=medecin_id,
            message=message,
            source = request.user.nom,
            destination = destination,
            admin_id=request.user.id
        )
        return redirect(f"/medecin/chat/{medecin_id}")
def chat_actif_admin_medecin(request,medecin_id):
    listeMedecin = Medecin.objects.all()
    messagesM = Messages_admin_medecin.objects.filter(medecin_id = medecin_id,admin_id=request.user.id)
    medecin = Medecin.objects.get(id=medecin_id);
    return render(request,"interfaceAdmin/interfaceChatMedecin.html",{"messagesM":messagesM,"medecin_actif":medecin,"listeMedecin":listeMedecin})

#chat entre admin et secretaire
class ChatEntreAdminSecretaire(View):
    def get(self,request):
        listSecretaire = Secretaire.objects.all();
        return render(request,"interfaceAdmin/interfaceChatSecretaire.html",{"listSecretaire":listSecretaire})
    def post(self,request):
        message = request.POST.get("message")
        secretaire_id = request.POST.get("secretaire_id")
        destination = request.POST.get("destination")
        Messages_admin_secretaire.objects.create(
            secretaire_id=secretaire_id,
            message=message,
            source = request.user.nom,
            destination = destination,
            admin_id=request.user.id
        )
        return redirect(f"/secretaire/chat/{secretaire_id}")
def chat_actif_admin_secretaire(request,secretaire_id):
    listeSecretaire = Secretaire.objects.all()
    messagesM = Messages_admin_secretaire.objects.filter(secretaire_id = secretaire_id,admin_id=request.user.id)
    secretaire = Secretaire.objects.get(id=secretaire_id);
    return render(request,"interfaceAdmin/interfaceChatSecretaire.html",{"messagesM":messagesM,"secretaire_actif":secretaire,"listSecretaire":listeSecretaire})


#chat medecin avec admin :
class MessageMedecinAdmin(View):
    def get(self,request):
        listAdmin = Administrateur.objects.all();
        return render(request,"interfaceMedecin/interfaceChatAdmin.html",{"listAdmin":listAdmin})
    def post(self,request):
        message = request.POST.get("message")
        admin_id = request.POST.get("admin_id")
        destination = request.POST.get("destination")
        Messages_admin_medecin.objects.create(
            medecin_id=request.user.id,
            message=message,
            source = request.user.nom,
            destination = destination,
            admin_id=admin_id
        )
        return redirect(f"/chat/admin/{admin_id}")
def chatActifAdminMedecin(request,admin_id):
    listeAdmin = Administrateur.objects.all()
    messagesM = Messages_admin_medecin.objects.filter(admin_id=admin_id,medecin_id=request.user.id)
    admin = Administrateur.objects.get(id=admin_id);
    return render(request,"interfaceMedecin/interfaceChatAdmin.html",{"messagesM":messagesM,"admin_actif":admin,"listAdmin":listeAdmin})

#chat secretaire avec admin :
class MessageMedecinSecretaire(View):
    def get(self,request):
        listAdmin = Administrateur.objects.all();
        return render(request,"interfaceSecretaire/interfaceChatAdmin.html",{"listAdmin":listAdmin})
    def post(self,request):
        message = request.POST.get("message")
        admin_id = request.POST.get("admin_id")
        destination = request.POST.get("destination")
        Messages_admin_secretaire.objects.create(
            secretaire_id=request.user.id,
            message=message,
            source = request.user.nom,
            destination = destination,
            admin_id=admin_id
        )
        return redirect(f"/chat/admin/secretaire/{admin_id}")
def chatActifAdminSecretaire(request,admin_id):
    listeAdmin = Administrateur.objects.all()
    messagesM = Messages_admin_secretaire.objects.filter(admin_id=admin_id,secretaire_id=request.user.id)
    admin = Administrateur.objects.get(id=admin_id);
    return render(request,"interfaceSecretaire/interfaceChatAdmin.html",{"messagesM":messagesM,"admin_actif":admin,"listAdmin":listeAdmin})


#afficher l'historique des rendez-vous
def afficherHistorique(request):
    listeRendezvous=RendezVous.objects.filter(patient_id=request.user.id)
    return render(request,"interfacePatient/historiqueRendezvous.html",{"listeRendezvous":listeRendezvous})

#ajouter demande de rendez-vous
class DemandePatient(View):
    def get(self,request,rendezvous_id):
        rendezvous=RendezVous.objects.get(id=rendezvous_id)
        return render(request,"pagedemande.html",{"rendezvous":rendezvous})
    def post(self,request,rendezvous_id):
        Demande.objects.create(
            objetDemande = request.POST.get("objetDemande"),
            bodyDemande = request.POST.get("bodyDemande"),
            patient_id = request.user.id,
            statut = "En Cours",
            rendezvous_id = rendezvous_id
        )
        messages.success(request,"Votre demande a été traité avec success")
        return redirect("historiqueRendezvous")

#afficher les rendez vous completes:
def afficherrendezvouscompletes(request):
    rendezVousValide = RendezVous.objects.filter(statut="Confirmé",patient_id=request.user.id)
    return render(request,"interfacePatient/historiqueRendezvous.html",{"rendezVousValide":rendezVousValide})
#afficher les rendez vous en cours:
def afficherrendezvousEncour(request):
    rendezvousencours = RendezVous.objects.filter(statut="En Cours",patient_id=request.user.id)
    return render(request,"interfacePatient/historiqueRendezvous.html",{"rendezvousencours":rendezvousencours})
#filtrer les rendez-vous
def filtrerrendezvous(request):
    nom = request.POST.get("nom")
    rendezvous = RendezVous.objects.filter(titreRendezVous = nom)
    return render(request,"interfacePatient/historiqueRendezvous.html",{"rendezvous":rendezvous})

#listedemandes
def listeDemandes(request):
    listedemandes = Demande.objects.all()
    return render(request,"interfaceSecretaire/listeDemande.html",{"listedemandes":listedemandes})
def filtrerdemande(request):
    nom = request.POST.get("nom")
    demande = Demande.objects.filter(objetDemande = nom)
    if demande.exists():
        return render(request,"interfaceSecretaire/listeDemande.html",{"demande":demande})
    else:
        messages.error(request,f"L'objet avec le nom {nom} ne contient pas")
        return redirect("listedemande")
def listeArchive(request):
    listeArchive = Archive.objects.all()
    return render(request,"interfaceSecretaire/listeArchive.html",{"listeArchive":listeArchive})
def validerdemande(request,demande_id):
    demande = Demande.objects.get(id=demande_id)
    demande.statut = "Confirmé"
    demande.save()
    message = (
        f"Bonjour,{demande.patient.nom} {demande.patient.prenom}"
        f" On a recu votre demande de rendez-vous {demande.rendezvous.titreRendezVous} !\n\n"
            f"Votre demande a été bien validé merci de venir prendre votre document \n"
            f" Merci et a bientot"
    )
    send_mail(
        from_email = "noreply@monsite.com",
        subject="Validation de rendez-vous",
        message= message,
        recipient_list=[demande.patient.email],
        fail_silently=False,
    )
    messages.success(request,"Demande confirmé avec success")
    return redirect("listedemande")
#filtrer archive:
def fitrerArchive(request):
    nom = request.POST.get("nom")
    archive = Archive.objects.filter(titreRendezVous = nom)
    if archive.exists():
        return render(request,"interfaceSecretaire/listeArchive.html",{"archive":archive})
    else:
        messages.error(request,f"L'objet avec le nom {nom} ne contient pas")
        return redirect("listearchive")