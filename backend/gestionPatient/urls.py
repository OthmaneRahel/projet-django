from django.urls import path
from . import views

urlpatterns=[
    path('',views.Home.as_view(),name='home'),
    # Routes Patient
    path('register/',views.register, name='register'),
    path('saveRendezvous/',views.saveRendezVous,name='saveform'),
    path('profil/<patient_id>',views.EditProfilPatient.as_view(), name='profilPatient'),
    path('FormPage/<patient_id>/<medecin_id>',views.FormPage.as_view(),name='formpatient'),
    path('listMedecins/',views.ListMedecin,name='medecin_list_page'),
    path('listMedecins/<medecin_id>',views.detailMedecin,name='detail_list_page'),
    path('historiqueRendezvous/',views.afficherHistorique,name='historiqueRendezvous'),
    path('ajouterdemande/<rendezvous_id>',views.DemandePatient.as_view(),name='demandepatient'),
    path('rendezvousComplet/',views.afficherrendezvouscompletes,name='rendezvouscomplet'),
    path('rendezvousEnCour/',views.afficherrendezvousEncour,name='rendezvousencour'),
    path('filtrerrendezvous/',views.filtrerrendezvous,name='filterrendezvous'),
    # Routes Medecin
    path('HomePageMedecin/',views.HomePageMedecin.as_view(), name='homePageMedecin'),
    path('register-medecin/',views.FormRegister.as_view(), name='registerMedecin'),
    #path('validation-register-medecin/',views.FormRegister.as_view(), name='validercreationCompte'),
    path('listRendezVous/',views.listRendezVous, name='homelistRendezvous'),
    path('listPatient/',views.listPatient, name='homelistPatient'),
    path('detail/<patient_id>',views.detailPatient, name='detailPatient'),
    path('profileMedecin/<id>',views.profileMedecin, name='ProfilMedecin'),
    path('detailRendezVous/<id>',views.detailRendezVous, name='detailRendezVous'),
    path('envoyerEmail/',views.envoyerEmail, name='EnvoyerEmail'),
    path('secretaires/messages',views.EnvoyerMessageAuSecretaire.as_view(), name='messageToSecretaire'),
    path('secretaire/messages/<secretaire_id>',views.messageMedecinAuSecretaire, name='chat_actif_medecin_secretaire'),
    path('chat/admins/',views.MessageMedecinAdmin.as_view(), name='chat_admin_medecin'),
    path('chat/admin/<admin_id>',views.chatActifAdminMedecin, name='chat_actif_admin_medecin'),
    path('rapport-medical/<rendezvous_id>',views.RapportMedical.as_view(), name='rapportMedical'),
    path('editProfilMedecin/<user_id>',views.EditProfilMedecin.as_view(), name='editProfil'),
    path('editdescriptionMedecin/<user_id>',views.EditDescriptionMedecin.as_view(), name='editdescription'),
    # Routes Secretaire :
    path('homePageSecretaire/',views.FormPageSecretaire, name='homePageSecretaire'),
    path('registerSecretaire/',views.FormRegisterSecretaire.as_view(), name='registerSecretaire'),
    path('rendez-vous/',views.listeRendez, name='rendezVous'),
    path('valider-rendez-vous/<rendezVous_id>',views.validerRendezVous, name='validerrendezvous'),
    path('envoyerMail/',views.envoyerEmailAuPatient, name='envoyerMail'),
    path('archiverRendezVous/<rendezVous_id>',views.archiverRendezVous, name='archiverRendezVous'),
    path('chat/admins/secretaire',views.MessageMedecinSecretaire.as_view(), name='chat_admin_sec'),
    path('chat/admin/secretaire/<admin_id>',views.chatActifAdminSecretaire, name='chat_actif_admin_secretaire'),
    path('editProfilSecretaire/<secretaire_id>',views.EditProfilSecretaire.as_view(), name='editProfilsecretaire'),
    path('medecins/messages/',views.EnvoyerMessageAuMedecin.as_view(), name='messageToMedecin'),
    path('messages/<medecin_id>',views.chatavecmedecin, name='chat_actif'),
    path('rendezvous/<id>',views.detailrendezvous, name='rendezvous'),
    path('construire-facture/<rendezvous_id>',views.construireFacture, name='construireFacture'),
    path('valider-facture/<rendezvous_id>',views.sauvegarderFacture, name='sauvegarderFacture'),
    path('listeDemande/',views.listeDemandes, name='listedemande'),
    path('demande/',views.filtrerdemande, name='filterdemande'),
    path('valider-demande/<demande_id>',views.validerdemande, name='validerdemande'),
    path('listeArchive/',views.listeArchive, name='listearchive'),
    path('archive/',views.fitrerArchive, name='filterarchive'),
    # Routes admin :
    path('homePageAdmin/',views.homePageAdmin, name='homepageadmin'),
    path('registerAdmin/',views.RegisterAdmin.as_view(), name='registeradmin'),
    path('listeMedecin/',views.ListMedecinAdmin.as_view(), name='listeMedecinAdmin'),
    path('medecin/<medecin_id>',views.supprimerMedecin, name='supprimerMedecin'),
    path('medecin-detail/<medecin_id>',views.detailMedecinAdmin, name='detailMedecinAdmin'),
    path('secretaire/<secretaire_id>',views.supprimerSecretaire, name='supprimerSecretaire'),
    path('secretaire-detail/<secretaire_id>',views.detailSecretaire, name='detailSecretaire'),
    path('listeSecretaire/',views.listesecretaire,name="listesecretaire"),
    path('secretaire/',views.filtrerSecretaire,name='filtrersecretaireparnom'),
    path('medecin/',views.filtrerMedecin,name='filtrermedecinparnom'),
    path('editProfiladmin/<user_id>',views.EditProfilAdmin.as_view(),name="profileadmin"),
    #chat entre admin et medecin :
    path('medecins/chat/',views.ChatEntreAdminMedecin.as_view(),name="messageEntreAdmintomedecin"),
    path('medecin/chat/<medecin_id>',views.chat_actif_admin_medecin,name="chat_actif_admin_medecin"),
    #chat entre admin et secretaire :
    path('secretaires/chat/',views.ChatEntreAdminSecretaire.as_view(),name="messageEntreAdmintosecretaire"),
    path('secretaire/chat/<secretaire_id>',views.chat_actif_admin_secretaire,name="chat_actif_admin_secretaire"),
    # Route pour marquer le message comme lu:
    path('marquer-comme-lu/<message_id>',views.MarquerMessageCommeLu, name='marquerCommeLu'),




    # Routes login page:
    path('auth/login/',views.LoginPage.as_view(), name='loginvalidation'),
    # path('auth/login/',views.LoginPage.as_view(),name='loginpage'),
    # Route Logout :
    path('logout/',views.logout_user,name='logout'),
    
]

