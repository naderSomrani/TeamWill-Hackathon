from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.parsers import FileUploadParser, MultiPartParser
import json
import datetime
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta


# Create your views here.


class TypeCreditAPI(APIView):
    def get(self, request):
        TCR_list = TypeCredit.objects.all().values()
        result = []
        for item in TCR_list:
            docID_list = LKTCRDOC.objects.filter(TCRID=item['id'])
            doc_tab = []
            for doc_item in docID_list:
                doc_tab.append(doc_item.DCRID)
            result_item = {
                'Type_Credit': item,
                'Documents': DocCreditSerializer(doc_tab, many=True).data
            }
            result.append(result_item)
        return Response(result, status=status.HTTP_200_OK)


class DocumentByIDCredit(APIView):
    def get(self, request ,id):
        lk_list = LKTCRDOC.objects.filter(TCRID=id).values()
        result = []
        doc_tab = []
        for item in lk_list:
            print(item['DCRID_id'])
            docID_list = DocCredit.objects.get(pk=item['DCRID_id'])
            result.append(docID_list)

        return Response(DocCreditSerializer(result, many=True).data, status=status.HTTP_200_OK)


class TypeCreditByIDAPI(APIView):
    def get(self, request, id):
        serializer = TypeCreditSerializer(TypeCredit.objects.get(pk=id))
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChampCreditAPI(APIView):
    def get(self, request):
        champ_list = LKTCRCHAMP.objects.filter(TCRID=request.query_params['TCRID'])
        champ_tab = []
        for champ_item in champ_list:
            champ_tab.append(champ_item.CCRID)
        return Response(ChampCreditSerializer(champ_tab, many=True).data, status=status.HTTP_200_OK)


class DossierProspectAPI(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        capital = int(body['DPRCAPITAL'])
        interet = float(body['DPRTAUXINTERET'])/100
        nbr_echance = int(body['DPRNBRECHEANCE'])
        total_interet = (capital * interet)
        echeance = (capital * interet/12) / (1-(1+interet/12)**(-nbr_echance))
        prospect = PROSPECT.objects.get(pk=body['PROCODE'])
        dpr_code = DOSSIERPROSPECT.objects.all().count()
        capital = capital + total_interet
        TCID = body['TCID']
        type_credit = TypeCredit.objects.get(pk=TCID)
        dossier_prospect = DOSSIERPROSPECT(DPRCODE=dpr_code+1, PROCODE=prospect, DPRCAPITAL=capital,
                                           DPRTAUXINTERET=interet, DPRTOTALINTERET=total_interet, DPRMENSUALITE=body['DPRMENSUALITE'],
                                           DPRNBRECHEANCE=nbr_echance, DPRECHEANCE=echeance, TCID=type_credit)
        dossier_prospect.save()
        CR = capital
        todayDate = datetime.date.today()
        print(todayDate.day)
        if todayDate.day > 25:
            todayDate = datetime.date(todayDate.year, todayDate.month+1, 25)
        else:
            todayDate = datetime.date(todayDate.year, todayDate.month, 25)
        print(todayDate)
        k = 1
        if dossier_prospect.DPRMENSUALITE == 'Mensuelle':
            k = 1
        elif dossier_prospect.DPRMENSUALITE == 'Trimestrielle':
            k = 3
        elif dossier_prospect.DPRMENSUALITE == 'Semestrielle':
            k = 6
        elif dossier_prospect.DPRMENSUALITE == 'Anuelle':
            k = 12
        for i in range(1, nbr_echance+1, k):
            In = CR * interet / 12
            Cn = echeance - In
            CR = CR - Cn
            dpr_echance = DPRECHEANCE(DPRORDER=i, DPRID=dossier_prospect, DPRINTERETN=In, DPRCAPITALN=Cn, DPRECHEANCEN=echeance, DPRDATE=todayDate)
            dpr_echance.save()
            if todayDate.month + k > 12:
                todayDate = datetime.date(todayDate.year+1, todayDate.month + k - 12, todayDate.day)
            else:
                todayDate = datetime.date(todayDate.year, todayDate.month+k, todayDate.day)
        print(dossier_prospect)
        serializer = DossierProspectSerializer(dossier_prospect, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SimulationEcheanceAPI(APIView):
    def get(self, request):
        serializer = DPRECHEANCESerializer(DPRECHEANCE.objects.filter(DPRID=request.query_params['ID']), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DPRCCRValeurAPI(APIView):
    def post(self, request):
        for dossier in request.data:
            serializer = DossierProspectSerializer(data=dossier)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoriqueProspectAPI(APIView):
    def get(self, request):
        serializer = DossierProspectSerializer(DOSSIERPROSPECT.objects.filter(PROCODE=request.query_params['PROCODE']), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DemandeCreditAPI(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, DCRID, DPRID, TCID, **kwargs):
        demande = DEMANDECREDIT(DPRID=DOSSIERPROSPECT.objects.get(pk=DPRID), DemCode="0001", TCID=TypeCredit.objects.get(pk=TCID))
        demande.save()
        data_demande = {
            "DCRID": DCRID,
            "DocumentFile": request.data["DocumentFile"],
            "DEMID": demande.id
        }
        file_serializer = DemandeSerializer(data=data_demande)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=204)


class ListDemande(APIView):
    def get(self, request):
        serializer = DEMANDECREDITSerializer(DEMANDECREDIT.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListDocumentDemande(APIView):
    def get(self, request):
        document = DEMANDECREDIT.objects.get(pk=request.query_params['ID'])
        serializer = DemandeSerializer(DOCUMENTDEMANDE.objects.filter(DEMID=document), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateETAT(APIView):
    def put(self, request, id):
        demande = DEMANDECREDIT.objects.get(pk=id)
        serializer = DEMANDECREDITSerializer(demande, data=request.data)
        if serializer.is_valid():
            serializer.save()

            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['cabannitaha@gmail.com', ]
            if demande.ETATDOCUMENT == 'Incomplet':
                subject = 'Refus de demande de crédit'
                message = 'Votre demande de crédit est refusé'
                send_mail(subject, message, email_from, recipient_list)
            if demande.ETATACCEPTATION == 'Accepté':
                subject = 'Acceptation de demande de crédit'
                message = 'Votre demande de crédit est accepté'
                send_mail(subject, message, email_from, recipient_list)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalculateScoreAPI(APIView):
    def get(self, request, id, DMID):
        prospect = PROSPECT.objects.get(pk=id)
        score = 0
        if prospect.PROAGE < 30 or prospect.PROAGE > 65:
            score = score + 0.1
        if prospect.PROSITUATIONFAMILLE != "Marie":
            score = score + 0.2
        if prospect.PROSALAIRE < 800:
            score = score + 0.2
        if prospect.PROFONCTION in ["Fonctionnaire", "Pas de fonction"]:
            score = score + 0.4
        if prospect.PRODIRIGENT == "Dirigent":
            score = score - 0.3
        if prospect.PRONBRENFANT > 2:
            score = score + 0.3
        if prospect.PROSECTEURFONCTION == "Privé":
            score = score + 0.2
        demande = DEMANDECREDIT.objects.get(pk=DMID)
        dossiers = DOSSIER.objects.filter(PROID=prospect)
        for item in dossiers:
            print("test1")
            if (item.DOSCAPITALRESTANT/demande.DPRID.DPRNBRECHEANCE) > (prospect.PROSALAIRE * 0.3):
                print("test2")
                score = score + 1
            dos_echeance = DOSECHEANCE.objects.filter(DOSID=item)
            for dos in dos_echeance:
                if dos.DATEECHEANCE < datetime.datetime.today():
                    if dos.DATEPAIEMENT is None:
                        score = score + 0.2
                    elif dos.DATEPAIEMENT > dos.DATEECHEANCE:
                        score = score + 0.1

        if score > 5:
            score = 5
        result = {
            "score": score
        }
        return Response(result, status=status.HTTP_200_OK)


class DemandeCompletAPI(APIView):
    def get(self, request):
        serializer = DEMANDECREDITSerializer(DEMANDECREDIT.objects.filter(ETATACCEPTATION="Complet"), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Registration(APIView):
    def post(self, request):
        username = request.data['username']
        password1 = request.data['password1']
        password2 = request.data['password2']
        if password1 != password2:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        email = request.data['PROMAIL']
        PROSPECT.objects.create(PRONOM=request.data['PRONOM'],
                            PROPRENOM=request.data['PROPRENOM'],
                            PRODEPRENOM=request.data['PRODEPRENOM'],
                            PROMAIL=email,
                            PROTEL=request.data['PROTEL'],
                            PRODATENAISS=datetime.datetime.strptime(request.data['PRODATENAISS'], "%Y-%m-%d").date(),
                            PROAGE=int(request.data['PROAGE']),
                            PROSITUATIONFAMILLE=request.data['PROSITUATIONFAMILLE'],
                            PROSALAIRE=float(request.data['PROSALAIRE']),
                            PROFONCTION=request.data['PROFONCTION'],
                            PROSECTEURFONCTION=request.data['PROSECTEURFONCTION'],
                            PRODIRIGENT=request.data['PRODIRIGENT'],
                            PRONBRENFANT=int(request.data['PRONBRENFANT']))
        user = User(username=username, email=email)
        user.set_password(password1)
        user.save()
        return Response(user.id, status= status.HTTP_200_OK)


class StatistiqueSimulation(APIView):
    def get(self, request):
        result = []
        last_month = datetime.today() - timedelta(days=30)
        for i in range(6):
            simulation = DOSSIERPROSPECT.objects.filter(DPRDATEPROCPECT__month=last_month.month)
            obj = {
                "month": last_month,
                "nbr_simulation": simulation.count()
            }
            result.append(obj)
            last_month = last_month - timedelta(days=30)
        return Response(result, status= status.HTTP_200_OK)


class StatistiqueDemandeCredit(APIView):
    def get(self, request):
        result = []
        last_month = datetime.today() - timedelta(days=30)
        for i in range(6):
            demandes = DEMANDECREDIT.objects.filter(DATE__month=last_month.month)
            obj = {
                "month": last_month,
                "nbr_demande": demandes.count()
            }
            result.append(obj)
            last_month = last_month - timedelta(days=30)
        return Response(result, status= status.HTTP_200_OK)


class StatistiqueDemandeCreditAccepte(APIView):
    def get(self, request):
        result = []
        last_month = datetime.today() - timedelta(days=30)
        for i in range(6):
            demandes = DEMANDECREDIT.objects.filter(DATE__month=last_month.month, ETATACCEPTATION='Accepté')
            obj = {
                "month": last_month,
                "nbr_demande": demandes.count()
            }
            result.append(obj)
            last_month = last_month - timedelta(days=30)
        return Response(result, status= status.HTTP_200_OK)