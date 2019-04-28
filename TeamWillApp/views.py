from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.parsers import FileUploadParser, MultiPartParser
import json
import datetime

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
        dossier_prospect = DOSSIERPROSPECT(DPRCODE=dpr_code+1, PROCODE=prospect, DPRCAPITAL=capital,
                                           DPRTAUXINTERET=interet, DPRTOTALINTERET=total_interet, DPRMENSUALITE=body['DPRMENSUALITE'],
                                           DPRNBRECHEANCE=nbr_echance, DPRECHEANCE=echeance)
        dossier_prospect.save()
        CR = capital
        todayDate = datetime.date.today()
        print(todayDate.day)
        if todayDate.day > 25:
            todayDate = datetime.date(todayDate.year, todayDate.month+1, 25)
        else:
            todayDate = datetime.date(todayDate.year, todayDate.month, 25)
        print(todayDate)
        for i in range(1, nbr_echance+1):
            In = CR * interet / 12
            Cn = echeance - In
            CR = CR - Cn
            dpr_echance = DPRECHEANCE(DPRORDER=i, DPRID=dossier_prospect, DPRINTERETN=In, DPRCAPITALN=Cn, DPRECHEANCEN=echeance, DPRDATE=todayDate)
            dpr_echance.save()
            if todayDate.month == 12:
                todayDate = datetime.date(todayDate.year+1, 1, todayDate.day)
            else:
                todayDate = datetime.date(todayDate.year, todayDate.month+1, todayDate.day)
        print(dossier_prospect)
        serializer = DossierProspectSerializer(dossier_prospect, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SimulationHistoriqueAPI(APIView):
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

    def post(self, request, DCRID, DPRID, **kwargs):
        demande = DEMANDECREDIT(DPRID=DOSSIERPROSPECT.objects.get(pk=DPRID), DemCode="0001")
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
