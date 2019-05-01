from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class TypeCredit(models.Model):
    TCRCODE = models.CharField(max_length=100)
    TCRNOM = models.CharField(max_length=100)
    TCRTAUXINTERT = models.FloatField()
    TCRDUREEMAX = models.IntegerField()
    TCRMAXCAPITAL = models.FloatField(default=0)
    TCRIMAGE = models.CharField(max_length=40, default="")


class DocCredit(models.Model):
    DCRCODE = models.CharField(max_length=100)
    DCRNOM = models.CharField(max_length=100)


class LKTCRDOC(models.Model):
    TCRID = models.ForeignKey(TypeCredit, on_delete=models.CASCADE)
    DCRID = models.ForeignKey(DocCredit, on_delete=models.CASCADE)


class ChampCredit(models.Model):
    CCRCODE = models.CharField(max_length=100)
    CCRNOM = models.CharField(max_length=100)
    CCRTYPE = models.CharField(max_length=100)


class LKTCRCHAMP(models.Model):
    TCRID = models.ForeignKey(TypeCredit, on_delete=models.CASCADE)
    CCRID = models.ForeignKey(ChampCredit, on_delete=models.CASCADE)


# class CustomUserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def create_user(self, PRONOM, PROPRENOM, PRODEPRENOM, PRODATENAISS, PROMAIL, PROTEL, password=None):
#         user = self.model(PRONOM, PROPRENOM, PRODEPRENOM, PRODATENAISS, PROMAIL, PROTEL)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_staffuser(self, ):
#         user = self.create_user(
#         )
#         user.is_staff = True
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, password):
#         user = self.create_user(
#
#         )
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


class PROSPECT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    PRONOM = models.CharField(max_length=100)
    PROPRENOM = models.CharField(max_length=100)
    PRODEPRENOM = models.CharField(max_length=100)
    PROMAIL = models.CharField(max_length=100)
    PROTEL = models.CharField(max_length=20)
    PRODATENAISS = models.DateField(null=True)
    PROAGE = models.IntegerField(default=0)
    PROSITUATIONFAMILLE = models.CharField(max_length=50, default="Marie")
    PROSALAIRE = models.FloatField(default=0)
    PROFONCTION = models.CharField(max_length=100,default="Salarie")
    PROSECTEURFONCTION = models.CharField(max_length=100, default="Public")
    PRODIRIGENT  = models.CharField(max_length=100,default="Dirigent")
    PRONBRENFANT = models.IntegerField(default=0)
    # username = models.CharField(max_length=255, default="")

    # USERNAME_FIELD = 'PROMAIL'
    # objects = CustomUserManager()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PROSPECT.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.prospect.save()

class DOSSIERPROSPECT(models.Model):
    DPRCODE = models.CharField(max_length=100)
    PROCODE = models.ForeignKey(PROSPECT, on_delete=models.CASCADE)
    DPRCAPITAL = models.FloatField()
    DPRTAUXINTERET = models.FloatField()
    DPRTOTALINTERET = models.FloatField()
    DPRMENSUALITE = models.CharField(max_length=100)
    DPRNBRECHEANCE = models.FloatField()
    DPRECHEANCE = models.FloatField()
    TCID = models.ForeignKey(TypeCredit, on_delete=models.CASCADE, null=True)
    DPRDATEPROCPECT = models.DateField(null=True)


class DPRCCRVALEUR(models.Model):
    DPRID = models.ForeignKey(DOSSIERPROSPECT, on_delete=models.CASCADE)
    CCRID = models.ForeignKey(ChampCredit, on_delete=models.CASCADE)
    VALEUR = models.CharField(max_length=100)


class DPRECHEANCE(models.Model):
    DPRORDER = models.IntegerField()
    DPRID = models.ForeignKey(DOSSIERPROSPECT, on_delete=models.CASCADE)
    DPRINTERETN = models.FloatField()
    DPRCAPITALN = models.FloatField()
    DPRECHEANCEN = models.FloatField()
    DPRDATE = models.DateField()


class DEMANDECREDIT(models.Model):
    DPRID = models.ForeignKey(DOSSIERPROSPECT, on_delete=models.CASCADE)
    DemCode = models.IntegerField()
    ETATACCEPTATION = models.CharField(max_length=50, default="En Attente")
    ETATDOCUMENT = models.CharField(max_length=50, default="En Attente")
    COMMENTAIREAGENT = models.CharField(max_length=255, default="En Attente")
    TCID = models.ForeignKey(TypeCredit, on_delete=models.CASCADE, null=True)
    DATE = models.DateField(null=True)


class DOCUMENTDEMANDE(models.Model):
    DCRID = models.ForeignKey(DocCredit, on_delete=models.CASCADE)
    DocumentFile = models.FileField(upload_to='./demande', null=True)
    DEMID = models.ForeignKey(DEMANDECREDIT, on_delete=models.CASCADE, null=True)


class DOSSIER(models.Model):
    DOSID = models.IntegerField()
    DOSCAPITAL = models.FloatField()
    DOSNBRECHEANCE = models.IntegerField()
    DOSCAPITALRESTANT = models.FloatField()
    PROID = models.ForeignKey(PROSPECT, on_delete=models.CASCADE, null=True)


class DOSECHEANCE(models.Model):
    DOSID = models.ForeignKey(DOSSIER, on_delete=models.CASCADE, null=True)
    ORDRE = models.IntegerField()
    DATEECHEANCE = models.DateField()
    MONTANTECHEANCE = models.IntegerField()
    DATEPAIEMENT = models.DateField(null=True, blank=True)
