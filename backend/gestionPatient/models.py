from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission


class Patient(AbstractBaseUser, PermissionsMixin):
    image = models.ImageField(null=True,blank=True,upload_to='patient/')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numeroTelephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=191, unique=True)
    adresse = models.TextField()
    cin = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='patient_set',
        blank=True,
        help_text='The groups this patient belongs to.',
        related_query_name='patient',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='patient_permissions',
        blank=True,
        help_text='Specific permissions for this patient.',
        related_query_name='patient',
    )
    REQUIRED_FIELDS = ['nom', 'prenom', 'numeroTelephone', 'cin']
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
class Medecin(AbstractBaseUser):
    image=models.ImageField(null=True,blank=True,upload_to='medecin/')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numeroTelephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=191, unique=True)
    profession = models.CharField(max_length=100)
    descriptionMedecin = models.TextField(max_length=100,default=True)
    cin = models.CharField(max_length=20, unique=True)
    salaire = models.FloatField()
    adresse = models.CharField(max_length=100,default=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    prix_consultation=models.IntegerField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ['nom', 'prenom', 'numeroTelephone', 'cin']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Secretaire(AbstractBaseUser):
    image=models.ImageField(null=True,blank=True,upload_to='secretaire/')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numeroTelephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=191, unique=True)
    adresse = models.CharField(max_length=255)
    cin = models.CharField(max_length=20, unique=True)
    salaire = models.FloatField()
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ['nom', 'prenom', 'numeroTelephone', 'cin']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Administrateur(AbstractBaseUser):
    image=models.ImageField(null=True,blank=True,upload_to='admin/')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numeroTelephone = models.CharField(max_length=20)
    email = models.EmailField(max_length=191, unique=True)
    adresse = models.CharField(max_length=255)
    cin = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ['nom', 'prenom', 'numeroTelephone', 'cin']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email



class RendezVous(models.Model):
    titreRendezVous = models.CharField(max_length=255)
    typeRendezVous = models.CharField(max_length=100)
    dateRendezVous = models.DateField()
    descriptionRendezVous = models.TextField(max_length=100,default=True)
    statut = models.CharField(max_length=30,default="En Cours")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendezvous', db_constraint=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='medecin', db_constraint=True,default=True)
    def __str__(self):
        return f"Rendez-vous {self.titreRendezVous} - {self.patient.email}"

class Facture(models.Model):
    prixFacture = models.FloatField()
    dateFacture = models.DateTimeField(default=timezone.now())
    note_supplementaire = models.TextField(max_length=150,default=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='factures', db_constraint=True)
    rendezvous = models.ForeignKey(RendezVous,on_delete=models.CASCADE,null=False,related_name='facture_rendezvous',db_constraint=True,default=True)
    def __str__(self):
        return f"Facture {self.id} - {self.patient.email}"

class Demande(models.Model):
    objetDemande = models.CharField(max_length=25)
    bodyDemande = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='demandes', db_constraint=True)
    statut = models.CharField(max_length=25,default=True)
    rendezvous = models.ForeignKey(RendezVous,on_delete=models.CASCADE,null=False,related_name='demande_rendezvous',db_constraint=True,default=True)

    def __str__(self):
        return f"Demande {self.objetDemande} - {self.patient.email}"
class Archive(models.Model):
        titreRendezVous = models.CharField(max_length=255)
        typeRendezVous = models.CharField(max_length=100)
        dateRendezVous = models.DateField()
        descriptionRendezVous = models.TextField(max_length=100,default=True)
        statut = models.CharField(max_length=30,default="False")
        patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendezvous_archive', db_constraint=True)
        medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='medecin_archive', db_constraint=True,default=True)
class Messages_secretaire_medecin(models.Model):
    source = models.CharField(max_length=30,default=False)
    destination = models.CharField(max_length=30,default=False)
    secretaire = models.ForeignKey(Secretaire,on_delete=models.CASCADE,related_name='secretaire_medecin',db_constraint=True)
    message = models.TextField(max_length=250,null=False)
    medecin = models.ForeignKey(Medecin,on_delete=models.CASCADE,related_name='medecin_secretaire',db_constraint=True)
    date_denvoi = models.DateTimeField(default=timezone.now())
    vu = models.BooleanField(default=False)
class RapportMedicalPatient(models.Model):
    prix = models.IntegerField(max_length=25);
    description = models.TextField(max_length=100);
    date_rapport = models.DateTimeField(default=timezone.now())
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='rapport_patient',db_constraint=True)
    medecin = models.ForeignKey(Medecin,on_delete=models.CASCADE,related_name='rapport_patient_medecin',db_constraint=True)
    rendezvous = models.ForeignKey(RendezVous,on_delete=models.CASCADE,null=False,related_name='rapports_rendezvous',db_constraint=True,default=True)
class Messages_admin_medecin(models.Model):
    source = models.CharField(max_length=30,default=False)
    destination = models.CharField(max_length=30,default=False)
    admin = models.ForeignKey(Administrateur,on_delete=models.CASCADE,related_name='admin_medecin',db_constraint=True)
    message = models.TextField(max_length=250,null=False)
    medecin = models.ForeignKey(Medecin,on_delete=models.CASCADE,related_name='medecin_admin',db_constraint=True)
    date_denvoi = models.DateTimeField(default=timezone.now())
    vu = models.BooleanField(default=False)
class Messages_admin_secretaire(models.Model):
    source = models.CharField(max_length=30,default=False)
    destination = models.CharField(max_length=30,default=False)
    secretaire = models.ForeignKey(Secretaire,on_delete=models.CASCADE,related_name='secretaire_admin',db_constraint=True)
    message = models.TextField(max_length=250,null=False)
    admin = models.ForeignKey(Administrateur,on_delete=models.CASCADE,related_name='admin_secretaire',db_constraint=True)
    date_denvoi = models.DateTimeField(default=timezone.now())
    vu = models.BooleanField(default=False)