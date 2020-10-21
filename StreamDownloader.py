import PySimpleGUI as sg
import json
import Sources
import os
import ffmpeg
from ffmpy import FFmpeg
import threading
import time
import shutil

def Check():
        down.join()
        global done
        done = 1
        

dbdir = os.path.dirname(os.path.realpath(__file__))
jsondb = '''{
                "Viktoria und Ihr Husar (2016)": "https://d279gtpur1viyb.cloudfront.net/O815996/0e2fce5c-dbe9-4f80-8106-8f02542dd481",
                "Max und Moritz": "https://d279gtpur1viyb.cloudfront.net/O815996/0e2fce5c-dbe9-4f80-8106-8f02542dd481",
                "Polnishe Hochzeit": "https://d279gtpur1viyb.cloudfront.net/O815952/0223f1f3-6833-4b35-881f-4f16d7378414",
                "Fidelio (2015)":"https://d279gtpur1viyb.cloudfront.net/A04050049/e12fb91e-8e40-477c-94c3-1649169611e7",
                "Fidelio (2008)": "https://d279gtpur1viyb.cloudfront.net/A95000925/adad7f61-32f9-42bd-aa56-77c69dac787e",
                "Fidelio (1970)": "https://d279gtpur1viyb.cloudfront.net/A05004485/4c5981bc-6b8a-4115-85fb-a264f28aedfe",
                "Fidelio (2007)": "https://d279gtpur1viyb.cloudfront.net/A93001722/5758a4ef-81a6-47ed-b58e-0c5888ede20d",

                "La sonnambula": "https://d279gtpur1viyb.cloudfront.net/A00009011/0467e56f-6d71-4d6c-aeff-fefe5e0fcec8",
                "Norma": "https://d279gtpur1viyb.cloudfront.net/A05015889/f9f6bbf5-98eb-40d6-9e31-c83bdeb84bf9",
                "Axel an der Himmelstur": "https://d279gtpur1viyb.cloudfront.net/O814975/e23484bc-feae-437a-a667-233264800db6",
                "Wozzeck": "https://d279gtpur1viyb.cloudfront.net/A04050082/2718f1f3-15f6-4700-9d37-4cbad4ba22b8",
                "Benvenuto Cellini": "https://d279gtpur1viyb.cloudfront.net/A04001504/3ba6142e-e78d-4fba-bc4d-46ad8647d629",
                "Les Troyens": "https://d279gtpur1viyb.cloudfront.net/A93001774/2ad0319f-563b-4f1d-aec7-aa515e3cc581",
                "Best of Bregenzer Festspiele":"https://d279gtpur1viyb.cloudfront.net/O815784/bd393a53-2865-4af3-a1f1-484ca98ecc10",

                "Carmen (2015)": "https://d279gtpur1viyb.cloudfront.net/A93001774/2ad0319f-563b-4f1d-aec7-aa515e3cc581",
                "Carmen (2010, Barcelona)": "https://d279gtpur1viyb.cloudfront.net/A93001791/70351810-8ec0-42b0-8803-56273ab76be0",
                "Carmen (2017)": "https://d279gtpur1viyb.cloudfront.net/A04050072/9baa8704-8bf2-44f1-91ce-1b284a5ecbbd",
                "Carmen (2010)": "https://d279gtpur1viyb.cloudfront.net/A04001532/33f49d4a-e6bb-40c6-83b5-109f771424b5",
                "Carmen (1967)": "https://d279gtpur1viyb.cloudfront.net/A05003129/671d5ad6-0922-4a4c-a441-04d320244296",

                "Mefistofele": "https://d279gtpur1viyb.cloudfront.net/A05050272/4bde74cf-4a6f-48ca-9aea-280a742f8268",
                
                "Pelléas et Mélisande": "https://d279gtpur1viyb.cloudfront.net/A01010807/82784c0e-d3c1-4f86-a6a5-9e6ab49a67bc",

                "Die Baden-Baden Operngala": "https://d279gtpur1viyb.cloudfront.net/A055505400000/0095498f-e390-4b11-8fa1-ad84971351ea]",

                "Die Csardasfurstin": "https://d279gtpur1viyb.cloudfront.net/A055503960000/6905bdba-c477-4294-869a-d887d8d898cf",
                "Die Lusrige Witwe": "https://d279gtpur1viyb.cloudfront.net/A055128550000/ea7a7dd0-777b-4041-8869-3b18b9d2efd7",
                "Don Giovanni in Nöten": "https://d279gtpur1viyb.cloudfront.net/F04005209/c3f23932-9758-43ce-bfb9-7c83a8ca8511",
                "Anna Bolena": "https://d279gtpur1viyb.cloudfront.net/A04001542/518c0f2c-1ae1-490c-8ad1-bb7745c1f11a",
                "L'elisir d'amore": "https://d279gtpur1viyb.cloudfront.net/O814469/36e352d7-6374-42e0-9134-b12d802e2141",
                "Roberto Devereux": "https://d279gtpur1viyb.cloudfront.net/A05015691/0251f4e8-bc67-4b31-8243-6bbb12df6461",
                "Rusalka": "https://d279gtpur1viyb.cloudfront.net/A05018371/255de34a-780e-4657-b490-7981ece809ab",
                "Andrea Chénier": "https://d279gtpur1viyb.cloudfront.net/A04001553/4aa9164a-c479-4cc4-9176-fadf8d86575d",
                "Fedora": "https://d279gtpur1viyb.cloudfront.net/A00007092/b6f36544-2599-4d60-be13-795be9cb902c",
                "Beatrice Cenci": "https://d279gtpur1viyb.cloudfront.net/A04050101/231639c7-cbe7-4480-9725-63a37d4969a2",
                "Roméo et Juliette": "https://d279gtpur1viyb.cloudfront.net/A04001512/dc87a420-51b2-4def-8f49-e5de668ed876",
                "Admeto": "https://d279gtpur1viyb.cloudfront.net/A05017271/cde29790-eb0f-43a5-a070-84e8a22f6271",
                "Ariodante": "https://d279gtpur1viyb.cloudfront.net/A04050084/cf751728-0f8d-4ff1-ac38-1e8e45cf9405",
                "Arminio": "https://d279gtpur1viyb.cloudfront.net/A05050434/c3334dff-639b-430a-ae57-d20c8b65130b",
                "Messiah": "https://d279gtpur1viyb.cloudfront.net/A04001515/9207cab5-3d07-480a-94b3-5aad741d893e",
                "Theodora": "https://d279gtpur1viyb.cloudfront.net/A04001521/497e5578-bd0c-40a5-af9b-ace54f16748e",
                "Il mondo della luna": "https://d279gtpur1viyb.cloudfront.net/A04001523/67a19523-5ee6-4b66-9222-558efc63551e",
                "Jedermann": "https://d279gtpur1viyb.cloudfront.net/A04050016/d7e821a9-b289-4216-affd-d38415d2a39b",
                "Jedermann (2020)": "https://d279gtpur1viyb.cloudfront.net/A04050134/8f07b0f1-b691-402a-a1a6-c8d4fff7eb5f",
                "Hänsel und Gretel (Film)": "https://d279gtpur1viyb.cloudfront.net/A05001666/421d661d-c03d-49a3-8830-b6839f418152",
                "Hänsel und Gretel": "https://d279gtpur1viyb.cloudfront.net/A04050047/1e468acc-48cc-49bd-8669-17f5c9e1c29e",
                "Die Sache Makropulos": "https://d279gtpur1viyb.cloudfront.net/A04001559/efd28ab1-c620-4313-be86-47e3c9f7ef4c",
                "Die Csárdásfürstin (1990)": "https://d279gtpur1viyb.cloudfront.net/O816008/4b4cbf02-79ff-4e0b-97e9-f10666eb67e7",
                "Die Csárdásfürstin (2002)": "https://d279gtpur1viyb.cloudfront.net/O816006/3646e652-27f9-4633-966f-9e40da900e7e",
                "Die Csárdásfürstin (2018)": "https://d279gtpur1viyb.cloudfront.net/O815878/bc08c245-95d6-4cc3-9d9d-666a91a6ffb7",
                "Gräfin Mariza (2004)": "https://d279gtpur1viyb.cloudfront.net/O816004/3fb76489-66cf-45b2-aecc-069d2b4cfe6d",
                "Gräfin Mariza (2018)": "https://d279gtpur1viyb.cloudfront.net/O815998/0968c359-392f-487a-b433-0a38fd480e81",
                "Gräfin Mariza (1987)": "https://d279gtpur1viyb.cloudfront.net/O816000/ba02b03b-9db7-407e-a5dd-f789f850bb1b",
                "Antonia und der Reißteufel": "https://d279gtpur1viyb.cloudfront.net/F042002/f900559a-3159-423a-85f1-467397c0b951",
                "Das Jagdgewehr": "https://d279gtpur1viyb.cloudfront.net/A04050102/bc88fece-0360-4b63-b744-efeb063c8910",
                "Das Land des Lächelns (2001)": "https://d279gtpur1viyb.cloudfront.net/O816007/9ca9c08a-0c0b-4df6-b696-62875632a1c6",
                "Das Land des Lächelns (1996)": "https://d279gtpur1viyb.cloudfront.net/F042005/460983ab-061d-43ac-afd4-429d112a38ba",
                "Das Land des Lächelns (2019)": "https://d279gtpur1viyb.cloudfront.net/O816047/fff90538-0535-4fd9-8ed3-077d31966caf",
                "Der Graf von Luxemburg": "https://d279gtpur1viyb.cloudfront.net/O816003/dd515345-b294-41f3-8999-d94f014a4b59",
                "Der Zarewitsch": "https://d279gtpur1viyb.cloudfront.net/O816002/eed81273-7de9-4df7-a7d4-f99a13ce8027",
                "Die Lustige Witwe": "https://d279gtpur1viyb.cloudfront.net/O811284/4442f191-01d6-493e-bbb5-dbbe6313dde3",
                "Giuditta": "https://d279gtpur1viyb.cloudfront.net/O816005/05eee130-9b2d-4b68-bcf3-fc93485fee29",
                "Zigeunerliebe (2019)": "https://d279gtpur1viyb.cloudfront.net/O816098/74408c07-84f7-48d1-978e-f9646e34b553",
                "Das Land des Lächelns (1989)": "https://d279gtpur1viyb.cloudfront.net/O816001/346656b9-5377-45e0-8d72-419a2cc7a687",
                "Pagliacci (1982)": "https://d279gtpur1viyb.cloudfront.net/A05005356/db8a1da4-9296-4579-8586-74038bea6c72",
                "Pagliacci (2015)": "https://d279gtpur1viyb.cloudfront.net/A04050043/1411f2c2-fe94-4619-a107-c2e1ff838102",
                "Cavalleria rusticana": "https://d279gtpur1viyb.cloudfront.net/A04050042/f0c46a9c-cd49-4e41-b12d-d69357e9c26b",
                "Don Quichotte (2019)": "https://d279gtpur1viyb.cloudfront.net/A04050115/5b704b10-decc-4050-90df-97448a14b91b",
                "Manon (2007, Berlin)": "https://d279gtpur1viyb.cloudfront.net/A05016414/268c78b9-30e9-419b-91c2-6aaa1386e634",
                "Manon (2007)": "https://d279gtpur1viyb.cloudfront.net/A04001500/c0d884d2-29b6-495e-8fef-c1e06410a406",
                "Don Quixote": "https://d279gtpur1viyb.cloudfront.net/A04050064/6423614a-576d-4162-b1ff-064e734ff806",
                "Halka": "https://d279gtpur1viyb.cloudfront.net/A04050122/739da1ec-e440-4d08-bda0-ded3302abab4",
                "Il ritorno d'Ulisse": "https://d279gtpur1viyb.cloudfront.net/A05004563/9fc384a9-826e-48e5-8bff-4ed09729fed8",
                "L'incoronazione di Poppea": "https://d279gtpur1viyb.cloudfront.net/A05004559/ec1828bd-efef-4eef-a4ba-a6049c212248",
                "L'Orfeo": "https://d279gtpur1viyb.cloudfront.net/A05000881/93010fe8-a7e9-4f88-9178-e700dab4f3a3",
                "L’incoronazione di Poppea": "https://d279gtpur1viyb.cloudfront.net/A04050103/7d9e6c8a-7b7c-44b5-b4bf-625fe5b93dad",
                "Apollo et Hyacinthus": "https://d279gtpur1viyb.cloudfront.net/A04001461/5201e4eb-c8df-471e-82a6-cd50d8f9e655",
                "Ascanio in Alba": "https://d279gtpur1viyb.cloudfront.net/A04001462/d5888f5e-3f1a-43be-b71f-5e2a8090573d",
                "Betulia liberata": "https://d279gtpur1viyb.cloudfront.net/A04001464/c6afc36e-7ce9-4ba1-a5ce-e2e33d797de2",
                "Così fan tutte (2020)": "https://d279gtpur1viyb.cloudfront.net/A04050133/1d5420f8-700d-47ca-abd4-70a21de41ef8",
                "Così fan tutte (1969)": "https://d279gtpur1viyb.cloudfront.net/A05004486/0d7ed608-5bf8-43ad-8a29-e2779eca4f98",
                "Così fan tutte (2013)": "https://d279gtpur1viyb.cloudfront.net/A04050015/9b57a5fa-e687-4fef-8ae5-3b5e0aed88d1",
                "Così fan tutte (2006)": "https://d279gtpur1viyb.cloudfront.net/A04001465/eacc2a82-d3a5-463d-90ea-323a9f23da4b",
                "Così fan tutte (2009)": "https://d279gtpur1viyb.cloudfront.net/A04001516/ff08d54b-9fc5-408f-98b0-aaf8768e1520",
                "Der Schauspieldirektor/Bastien und Bastienne": "https://d279gtpur1viyb.cloudfront.net/A04500448/bb9043f1-bbff-46aa-abad-dd09a92da2a9",
                "Die Entführung aus dem Serail": "https://d279gtpur1viyb.cloudfront.net/A05004570/32fbc359-dec7-4b24-bce6-d6cd8575dc05",
                "Die Entführung aus dem Serail": "https://d279gtpur1viyb.cloudfront.net/A04001470/0bb3dcd8-aaef-4794-a4d5-cba6869be9db",
                "Die Entführung aus dem Serail (2013)": "https://d279gtpur1viyb.cloudfront.net/A04050014/38ac5ad2-cd09-4f18-b59e-7a5a51cae3a1",
                "Die Schuldigkeit des ersten Gebots": "https://d279gtpur1viyb.cloudfront.net/A04001466/f706b7d3-bf6a-4e7d-a321-55426ea06bda",
                "Die Zauberflöte (1983)": "https://d279gtpur1viyb.cloudfront.net/A05004608/ec53296d-d0d1-4c45-b992-37f5859a0287",
                "Die Zauberflöte (2006)": "https://d279gtpur1viyb.cloudfront.net/A04001468/fbb153af-835d-446a-b778-725c21e5ca8a",
                "Die Zauberflöte (2018)": "https://d279gtpur1viyb.cloudfront.net/A04050092/36052197-5dd8-4f8f-be22-bf6f09fd394f",
                "Die Zauberflöte (2012)": "https://d279gtpur1viyb.cloudfront.net/A04001579/ab96e152-d775-463a-b4d8-45926adc85f2",
                "Die Zauberflöte (2013)": "https://d279gtpur1viyb.cloudfront.net/A04050007/26bce17c-1fbb-4b12-828d-acb27dd676c1",
                "Die Zauberflöte for Children":"https://d279gtpur1viyb.cloudfront.net/O812962/d3bb312c-111e-414f-b832-0bb51aad0de7",
                "Don Giovanni (2006)":"https://d279gtpur1viyb.cloudfront.net/A04001469/5e1e3224-90ff-4ca1-8304-0c5861436a05",
                "Don Giovanni (2014)":"https://d279gtpur1viyb.cloudfront.net/A04050033/7f02c5d5-119a-42d1-8103-41f3d561c891",
                "Don Giovanni (1954)":"https://d279gtpur1viyb.cloudfront.net/A02000279/aea43911-058a-48f0-b8f5-3cb81732e1e3",
                "Don Giovanni (2008)":"https://d279gtpur1viyb.cloudfront.net/A04001510/73f1cd01-7416-4b10-a9be-91ca9623ac9e",
                "Idomeneo (2006)":"https://d279gtpur1viyb.cloudfront.net/A04001471/082cfd67-75c9-49c7-8a03-0c83bc16b09e",
                "Il re pastore":"https://d279gtpur1viyb.cloudfront.net/A04001475/c0dbdbe6-77a4-462b-86de-47bae84ae606",
                "Il sogno di Scipione":"https://d279gtpur1viyb.cloudfront.net/A04001476/d0a02d6e-5b0a-43dc-b94e-2ed26236f367",
                "Irrfahrten 2 (II): Abendempfindung":"https://d279gtpur1viyb.cloudfront.net/A04001460/c3344adb-6987-4846-a6e9-7682cd0c4fa7",
                "Irrfahrten 3 (III): Rex tremendus (L'oca del Cairo - Lo sposo deluso)":"https://d279gtpur1viyb.cloudfront.net/A045004500000/47cc4189-ec0b-4a0f-8ecb-e2c63821a572",
                "La clemenza di Tito (2006)":"https://d279gtpur1viyb.cloudfront.net/A04001477/bc7fb37c-ae6b-4146-b8a6-40c77c799d2c",
                "La clemenza di Tito (1980)":"https://d279gtpur1viyb.cloudfront.net/A05001697/8a3eeb97-bea1-46eb-bb0e-dff56c20b840",
                "La clemenza di Tito (2017)":"https://d279gtpur1viyb.cloudfront.net/A04050078/6fe491cf-f096-484e-a295-6f80abb063f8",
                "La finta giardiniera":"https://d279gtpur1viyb.cloudfront.net/A04001446/d9b19e4a-057c-44ce-ad41-b26a8628a57c",
                "La finta semplice":"https://d279gtpur1viyb.cloudfront.net/A04001478/af5af3a9-ec3e-4af1-b3f5-743778d55802",
                "Le nozze di Figaro (1976)":"https://d279gtpur1viyb.cloudfront.net/A05002158/5fa20f7b-85f3-4fb9-b1b2-7b81c9b2f0d3",
                "Le nozze di Figaro (2006)":"https://d279gtpur1viyb.cloudfront.net/A04001479/b39ec048-39ee-4093-8b89-21026e14d918",
                "Le nozze di Figaro (2015)":"https://d279gtpur1viyb.cloudfront.net/A04050050/3b103c03-d49a-471b-9f00-b304faf51a04",
                "Lucio Silla":"https://d279gtpur1viyb.cloudfront.net/A04001480/42003bc7-9384-4cc9-a01f-45ff68bdb4c8",
                "Mitridate, re di Ponto":"https://d279gtpur1viyb.cloudfront.net/A04001481/4f985d1d-2e85-4197-947f-0e3879ffb0b5",
                "Pùnkitititi!":"https://d279gtpur1viyb.cloudfront.net/F040038/d5fe757c-29dc-44bd-947e-ae3e0f1d0447",
                "Die schöne Helena":"https://d279gtpur1viyb.cloudfront.net/A05004529/5f1e7e24-549e-49bd-9942-c77b01f9365f",
                "Les Contes d'Hoffmann (2015)":"https://d279gtpur1viyb.cloudfront.net/A04050051/999a8109-bd98-471f-9fef-60de3b64e853",
                "Les contes d'Hoffmann (2019)":"https://d279gtpur1viyb.cloudfront.net/O816119/1879772f-d7d2-4c08-8eac-e89bb57bc3f8",
                "Orphée aux enfers":"https://d279gtpur1viyb.cloudfront.net/A04050113/6f0f038c-31d8-4be3-a243-0b86665a4e2f",
                "Der feurige Engel":"https://d279gtpur1viyb.cloudfront.net/A01050094/014ba850-80d4-4c39-be6a-eb3f541984e4",
                "La Bohème (1989)":"https://d279gtpur1viyb.cloudfront.net/F030002/7ca00ccc-0433-4e52-b8f2-b54fbed4baf0",
                "La Bohème (1965)":"https://d279gtpur1viyb.cloudfront.net/A05003130/fec9ec90-517a-4fec-81c2-70a363d40800",
                "La Bohème (2012)":"https://d279gtpur1viyb.cloudfront.net/A04001582/57d9db02-dd2c-4188-a355-df98b45c579a",
                "La fanciulla del West":"https://d279gtpur1viyb.cloudfront.net/A04050024/4c23c56a-25a6-4adc-a53f-de39e1c1092b",
                "Madama Butterfly":"https://d279gtpur1viyb.cloudfront.net/A05004539/160d1714-6aa0-49b5-b620-681fd8c3f6de",
                "Tosca (2010)":"https://d279gtpur1viyb.cloudfront.net/A05018154/6d76c2f5-3dd4-487b-a56e-7a5b0a6d1060",
                "Tosca (2018)":"https://d279gtpur1viyb.cloudfront.net/A04050088/c8dd7954-7a0f-4307-a48c-8af920280a3a",
                "Tosca (1976)":"https://d279gtpur1viyb.cloudfront.net/A05004543/e4ca3590-2e7f-4898-b376-5b08cd066393",
                "Tosca (2015)":"https://d279gtpur1viyb.cloudfront.net/ORF0034/92504965-22c3-4b04-a9ac-947eb9ad67eb",
                "Turnadot (2008)":"https://d279gtpur1viyb.cloudfront.net/A93001747/f7d0b346-788b-4c88-9636-e48cb8481909",
                "Turnadot (2015)":"https://d279gtpur1viyb.cloudfront.net/A04050045/ad9563de-d1c4-4606-8e90-0f888e571850",
                "Die Zarenbraut":"https://d279gtpur1viyb.cloudfront.net/A05050112/f82699bf-2a36-4027-8d7c-b93b820dfbe0",
                "William Tell (2016)":"https://d279gtpur1viyb.cloudfront.net/O814784/6af5767a-3071-49b5-85ac-4fc6921b83e7",
                "William Tell (2013)":"https://d279gtpur1viyb.cloudfront.net/A00050013/7da88e7f-c140-4e24-bbe2-d97a890830be",
                "Il Barbiere di Siviglia":"https://d279gtpur1viyb.cloudfront.net/A05001931/0923bcbb-e8fc-4863-bd82-f95aa5e85214",
                "L'italiana in Algeri":"https://d279gtpur1viyb.cloudfront.net/A04050104/dd407b72-1fe1-4f30-958d-cfc13ddd5490",
                "La Cenerentola (1981)":"https://d279gtpur1viyb.cloudfront.net/A05001906/da30cc63-bf69-4311-be8d-7f3e80a2fc58",
                "La Cenerentola (2008)":"https://d279gtpur1viyb.cloudfront.net/A93001741/36cd9e7c-8f74-4fb1-8d9e-a6fa72cff359",
                "La scala di seta":"https://d279gtpur1viyb.cloudfront.net/A00008824/0313b21c-4980-47fc-be1c-e804d3b5f4dc",
                "Mosè in Egitto":"https://d279gtpur1viyb.cloudfront.net/A04050076/c4ef1ed5-086c-43df-ad2c-7da6bd471740",
                "Fierrabras":"https://d279gtpur1viyb.cloudfront.net/A04050032/c8018bff-64d0-4221-95bf-a6e0caf4a7d8",
                "Der Zigeunerbaron (2000)":"https://d279gtpur1viyb.cloudfront.net/O812124/8f33e3fb-a1b2-4ebc-a0d8-0f227e3629fc",
                "Der Zigeunerbaron (2020)":"https://d279gtpur1viyb.cloudfront.net/O816340/d8777095-60f1-41c9-9005-7eff37687372",
                "Der Zigeunerbaron (2011)":"https://d279gtpur1viyb.cloudfront.net/O812296/2693522c-ab0c-48c9-8866-f7fade92f552",
                "Der Zigeunerbaron (1986)":"https://d279gtpur1viyb.cloudfront.net/O815999/76f305f3-e766-4b04-8f56-71e83ebb2f9f",
                "A Midsummer Night's Dream":"https://d279gtpur1viyb.cloudfront.net/A04050017/66d8eb8a-233c-4952-868e-4b6748431eaf",
                "Die Fledermaus (1986)":"https://d279gtpur1viyb.cloudfront.net/A05006298/ad181a22-6e41-41d2-b3fc-9e011ebe9566",
                "Die Fledermaus (1972)":"https://d279gtpur1viyb.cloudfront.net/A05004507/1c345a31-2a02-4818-9d65-bc70165056e9",
                "Die Fledermaus (1996)":"https://d279gtpur1viyb.cloudfront.net/O812723/e7c0b3bc-503f-4d7a-b499-547698632b6a",
                "Die Fledermaus (2012)":"https://d279gtpur1viyb.cloudfront.net/O813231/3b9a1e95-e59d-4761-a9b5-76fb20b4fe3a",
                "Eine Nacht in Venedig (1988)":"https://d279gtpur1viyb.cloudfront.net/O810606/f533c97a-4a38-47fa-8be6-5a0a165f4313",
                "Eine Nacht in Venedig (2015)":"https://d279gtpur1viyb.cloudfront.net/O815995/571ded96-7ffa-4a06-b7fa-7ed54912bc47",
                "Eine Nacht in Venedig (1999)":"https://d279gtpur1viyb.cloudfront.net/O811423/74637a59-c135-482d-a1d6-56eaa55988b6",
                "Ariadne auf Naxos (2012)":"https://d279gtpur1viyb.cloudfront.net/A04001581/3dde3ec9-abf6-4e20-a604-1e02e80ea1b2",
                "Die Frau ohne Schatten":"https://d279gtpur1viyb.cloudfront.net/A04001554/c9811f02-d944-4edd-8aad-cfbb9ea165d1",
                "Elektra (2010)":"https://d279gtpur1viyb.cloudfront.net/A04001539/d67c0ef8-366b-4094-8521-99a683429580",
                "Elektra (2020)":"https://d279gtpur1viyb.cloudfront.net/A04050132/ef271d3d-4cf5-4f0d-9813-a9c84c0e7ee2",
                "Arabella":"https://d279gtpur1viyb.cloudfront.net/A04050027/bd393f22-7932-4c74-ade8-fbd096317f26",
                "Ariadne auf Naxos (2006)":"https://d279gtpur1viyb.cloudfront.net/A95000924/bed7827d-e0ea-4bc6-9ce1-861be5b0b837",
                "Der Rosenkavalier":"https://d279gtpur1viyb.cloudfront.net/A04050031/baaabeca-576d-4ab4-993b-2153b4291373",
                "Salome":"https://d279gtpur1viyb.cloudfront.net/A04050093/4f6ba370-de92-42a4-a9f5-e522e55058c1",
                "Der Kaufmann von Venedig":"https://d279gtpur1viyb.cloudfront.net/A04050019/40527444-50ad-4933-99a9-c47433b9d642",
                "Pique Dame (2018)":"https://d279gtpur1viyb.cloudfront.net/A04050094/620012d9-2392-4357-a129-1d24ed0b56b7",
                "Pique Dame (2016)":"https://d279gtpur1viyb.cloudfront.net/A86050015/a6ccc182-cf69-485d-b012-cf1a0038458d",
                "Aida (2012)":"https://d279gtpur1viyb.cloudfront.net/A00009000/7f971385-2669-4450-b815-b7a0f22fd6f6",
                "Aida (2015)":"https://d279gtpur1viyb.cloudfront.net/A00050020/7611ded5-947f-4e5e-8494-de954a056874",
                "Aida (2017)":"https://d279gtpur1viyb.cloudfront.net/A04050077/c7db03dc-bb13-4f78-b495-09ed583afbdd",
                "Aida (2014)":"https://d279gtpur1viyb.cloudfront.net/ORF0032/5ffd3200-20d9-4521-bcd6-0a924bcb766e",
                "Aida (2009)":"https://d279gtpur1viyb.cloudfront.net/A04001520/6ae9e9de-7401-4d8a-83ab-0d3bcbfc8baa",
                "Alzira":"https://d279gtpur1viyb.cloudfront.net/A00008999/0dd57440-ed13-4195-996f-275be240e0b5",
                "Attila":"https://d279gtpur1viyb.cloudfront.net/A00008957/2c67f0ef-9cca-4223-aae5-a7917865d03b",
                "Don Carlo (2013)":"https://d279gtpur1viyb.cloudfront.net/A04050012/c2639b2c-054f-42c9-bd61-64f840f037ea",
                "Don Carlo (2012)":"https://d279gtpur1viyb.cloudfront.net/A00008989/0feda66d-b69d-46f1-881a-5992eafeeff7",
                "Ernani":"https://d279gtpur1viyb.cloudfront.net/A00008990/2b41e44e-7602-4ad9-9819-493a8a866d2e",
                "Falstaff (2013)":"https://d279gtpur1viyb.cloudfront.net/A04050010/c93bb0a3-79ba-4616-8130-1cdcd900215c",
                "Falstaff (2011)":"https://d279gtpur1viyb.cloudfront.net/A00008983/a4c1ec1b-a1fe-4650-be30-ffe93baee5fc",
                "Falstaff (2011, Zürich)":"https://d279gtpur1viyb.cloudfront.net/A95000922/665415a1-3a2c-498f-b5dd-3f224f75b999",
                "Falstaff (1979)":"https://d279gtpur1viyb.cloudfront.net/A05005352/c445ccc1-ef73-4972-893a-4b5187000824",
                "Giovanna d'Arco (2008)":"https://d279gtpur1viyb.cloudfront.net/A00008881/e294d296-1849-4841-a06d-40b7fa777dd9",
                "Giovanna d'Arco (2016)":"https://d279gtpur1viyb.cloudfront.net/A00050042/451c44c1-6751-49de-92a5-e51684d7006a",
                "I due Foscari (2016)":"https://d279gtpur1viyb.cloudfront.net/A00050037/b2b466f8-30ee-4382-908c-11cac93b9330",
                "I due Foscari (2009)":"https://d279gtpur1viyb.cloudfront.net/A00008846/740a0fec-707c-4cec-90de-2417b128c51b",
                "I Lombardi alla prima crociata":"https://d279gtpur1viyb.cloudfront.net/A00008886/260f2805-106e-4d0f-8423-df0b8f7974e4",
                "I masnadieri":"https://d279gtpur1viyb.cloudfront.net/A00008998/2c4c87a6-50f1-4c33-9fe3-017aa93d575e",
                "I vespri siciliani":"https://d279gtpur1viyb.cloudfront.net/A00008958/c0f22194-0e44-4f24-b24e-ff565c94ea88",
                "Il Corsaro":"https://d279gtpur1viyb.cloudfront.net/A00008882/aa60f47e-234b-4d57-b059-cf7d210e1496",
                "Il Trovatore (2013)":"https://d279gtpur1viyb.cloudfront.net/A05050142/ac8e8cd2-42fd-4c4d-8b26-2a63185b777d",
                "Il Trovatore (2010)":"https://d279gtpur1viyb.cloudfront.net/A00008956/30e65e59-f79e-4cf4-8194-a809e7b47626",
                "Il Trovatore (2014)":"https://d279gtpur1viyb.cloudfront.net/A04050025/6449fa31-f58c-4be6-b988-e9949cd75fac",
                "La battaglia di Legnano":"https://d279gtpur1viyb.cloudfront.net/A00009010/7ddce2d6-c79e-449f-813c-445206ce1b4c",
                "La forza del destino (2008)":"https://d279gtpur1viyb.cloudfront.net/A04001535/820a0189-bffb-4f42-ac54-afb33247ef69",
                "La forza del destino (2011)":"https://d279gtpur1viyb.cloudfront.net/A00008963/f2e12019-3387-4d8f-9a59-80386f803c5b",
                "La forza del destino (2014)":"https://d279gtpur1viyb.cloudfront.net/A05050169/6ce2cd96-bf81-4c88-930d-40ef585b0534",
                "La Traviata (2015)":"https://d279gtpur1viyb.cloudfront.net/A05050236/529ee420-2275-47b0-8633-ad2ae97aa94d",
                "La Traviata (2007)":"https://d279gtpur1viyb.cloudfront.net/A00008991/302f4820-aed4-4faf-a657-b83039e860a5",
                "Luisa Miller":"https://d279gtpur1viyb.cloudfront.net/A00008711/6461fa33-6ecb-46ac-a916-968722a04ae6",
                "Macbeth":"https://d279gtpur1viyb.cloudfront.net/A00008996/4b7c5e45-ffd9-4b5a-a5a3-875430a088df",
                "Nabucco (2007)":"https://d279gtpur1viyb.cloudfront.net/A00008685/b9abc754-94cc-44ec-abb6-8dc02fa4aaf9",
                "Nabucco (2009)":"https://d279gtpur1viyb.cloudfront.net/A00008847/7fcfb25e-f579-4ff3-ae45-67786bcd7cf6",
                "Oberto, Conte di San Bonifacio":"https://d279gtpur1viyb.cloudfront.net/A00008995/b0d9a734-c73d-455f-a046-48bbcafd8326",
                "Otello (2008)":"https://d279gtpur1viyb.cloudfront.net/A04001511/b5331fec-2e1c-49d9-9330-80f62d126e00",
                "Otello (2016)":"https://d279gtpur1viyb.cloudfront.net/A04050055/72bc309f-d7b9-43e4-9c4f-aad6dc9cd579",
                "Otello (1973)":"https://d279gtpur1viyb.cloudfront.net/A05004522/a9676691-4d9b-4bbc-a69f-28478c132628",
                "Rigoletto (1982)":"https://d279gtpur1viyb.cloudfront.net/A05004577/fa9a6879-cbb9-4da5-9d06-3218e4d38336",
                "Rigoletto (2019)":"https://d279gtpur1viyb.cloudfront.net/A04050112/f805262d-a0dc-475c-845b-409effc0a2c3",
                "Rigoletto (2008)":"https://d279gtpur1viyb.cloudfront.net/A00008993/fc7bca50-d10d-4f57-aa31-e1ef7d51db13",
                "Rigoletto (2017)":"https://d279gtpur1viyb.cloudfront.net/O815045/87f8ac07-2d35-44ce-9215-0f6e26042ee9",
                "Simon Boccanegra (2019)":"https://d279gtpur1viyb.cloudfront.net/A04050116/54f9c6db-2651-47ac-88e8-ce9793038d4d",
                "Simon Boccanegra (2010)":"https://d279gtpur1viyb.cloudfront.net/A00008884/49434033-b3e6-4286-83c2-a23f19290363",
                "Stiffelio":"https://d279gtpur1viyb.cloudfront.net/A00008992/4cebddd8-700c-4ec4-9932-7cd171ce82f8",
                "Un ballo in maschera (2011)":"https://d279gtpur1viyb.cloudfront.net/A00008984/69598943-f9f4-49d0-a1a1-525f1e04185d",
                "Un ballo in maschera (2016)":"https://d279gtpur1viyb.cloudfront.net/A05050309/54846380-97c5-4819-9d40-964e1088a148",
                "Un giorno di regno":"https://d279gtpur1viyb.cloudfront.net/A00008883/ad987704-33ea-4986-a1a7-d65bc6d23cee",
                "Die fünfte Jahreszeit":"https://d279gtpur1viyb.cloudfront.net/F042007/07a91b89-7d64-4023-835d-ce6091214127",
                "Das Rheingold (1980)":"https://d279gtpur1viyb.cloudfront.net/A05004571/238dc5aa-1b57-4ab0-b09c-12d5cd800034",
                "Das Rheingold (1991)":"https://d279gtpur1viyb.cloudfront.net/A05008443/6dfb183f-03d1-4732-be19-2da5eadb7347",
                "Das Rheingold (1980, Bayreuth)":"https://d279gtpur1viyb.cloudfront.net/A05004567/ed372645-8b09-470f-905c-629bbd730a7c",
                "Der fliegende Holländer (1974)":"https://d279gtpur1viyb.cloudfront.net/A05004533/7ed2c95e-59fc-4666-a6b4-b2ee28104304",
                "Der fliegende Holländer (1985)":"https://d279gtpur1viyb.cloudfront.net/A05004637/c327de54-b027-492b-96de-8a3b56d77083",
                "Die Meistersinger von Nürnberg (2008)":"https://d279gtpur1viyb.cloudfront.net/A04001509/c45b0206-d32e-4fa7-a750-26482c6cd181",
                "Die Meistersinger von Nürnberg (1999)":"https://d279gtpur1viyb.cloudfront.net/A05012420/1796561c-d9bb-4bf1-898e-3b3ab6657512",
                "Die Meistersinger von Nürnberg (2013)":"https://d279gtpur1viyb.cloudfront.net/A04050011/11366bfc-3fd0-4ad1-afb7-80f566094163",
                "Die Meistersinger von Nürnberg (1984)":"https://d279gtpur1viyb.cloudfront.net/A05004621/00384b40-5992-4330-b68b-53d1f814cc34",
                "Die Walküre (1980)":"https://d279gtpur1viyb.cloudfront.net/A05004568/0e8ed5b7-d5aa-4772-9270-bccb0f03a20b",
                "Die Walküre (2017)":"https://d279gtpur1viyb.cloudfront.net/A04050067/a5f28b79-98bc-4830-bd64-034502a30109",
                "Die Walküre (1992)":"https://d279gtpur1viyb.cloudfront.net/A05008445/15b49f03-817a-4aa7-84e8-c964494baa43",
                "Götterdämmerung (1991)":"https://d279gtpur1viyb.cloudfront.net/A05008444/004b4589-56e5-44b7-911f-483efa6dcdc2",
                "Götterdämmerung (1979)":"https://d279gtpur1viyb.cloudfront.net/A05004566/a9e86ebb-b470-4fd9-8684-c17f11b2ed25",
                "Götterdämmerung (Mehta/La Fura dels Baus/Valencia)":"https://d279gtpur1viyb.cloudfront.net/A93001742/3dfadc2a-ab89-4645-8c73-67c52b7f94eb",
                "Lohengrin (2016)":"https://d279gtpur1viyb.cloudfront.net/A05050310/34ff7dbc-55d4-4bca-b63c-0a7195a73088",
                "Lohengrin (1990)":"https://d279gtpur1viyb.cloudfront.net/A05007734/2b3ff2b0-2e25-450a-ad81-546970f94652",
                "Lohengrin (1982)":"https://d279gtpur1viyb.cloudfront.net/A05004586/c6a5682f-b374-418d-a861-eb14d4c6cc98",
                "Lohengrin (2009)":"https://d279gtpur1viyb.cloudfront.net/A05017478/272e5cde-3e69-4c61-afe1-1540bfe23d62",
                "Parsifal (1998)":"https://d279gtpur1viyb.cloudfront.net/A05011521/3ba93b7c-89ce-444c-a948-729f4f51262b",
                "Parsifal (2014)":"https://d279gtpur1viyb.cloudfront.net/A04050005/b5b3f8ae-c335-4500-aaac-c9a93577057f",
                "Parsifal (1981)":"https://d279gtpur1viyb.cloudfront.net/A05004576/b2f46a02-670c-4bfc-bb1e-d63255752b0f",
                "Rienzi":"https://d279gtpur1viyb.cloudfront.net/A05017663/e990ec77-6d67-4edc-b248-0f6c8cb223f7",
                "Siegfried (1992)":"https://d279gtpur1viyb.cloudfront.net/A05008446/512ce892-3029-4b9e-9959-508e1d1ed967",
                "Siegfried (1980)":"https://d279gtpur1viyb.cloudfront.net/A05004569/82104941-c7f0-4d7a-9a92-1952f2ab7e16",
                "Tannhäuser (1978)":"https://d279gtpur1viyb.cloudfront.net/A05004557/8ff436b5-b0db-4237-8e07-472c0cc01e54",
                "Tannhäuser (2014)":"https://d279gtpur1viyb.cloudfront.net/A05050163/02a082fe-7077-4488-a11d-1599a9912ecf",
                "Tannhäuser (2008)":"https://d279gtpur1viyb.cloudfront.net/A93001792/85576638-3c73-4eed-807d-17225553ddae",
                "Tannhäuser (1989)":"https://d279gtpur1viyb.cloudfront.net/A05007037/b086b1f8-ab72-4612-85e1-3bdf98c6a2e0",
                "Tristan und Isolde (1995)":"https://d279gtpur1viyb.cloudfront.net/A05009688/a6f9953d-fefb-466c-9731-77075258314f",
                "Tristan und Isolde (1983)":"https://d279gtpur1viyb.cloudfront.net/A05004610/04627e23-6868-48bf-bc59-b4947c40f5ba",
                "Tristan und Isolde (2018)":"https://d279gtpur1viyb.cloudfront.net/A05050584/604d27de-51cc-4b1a-8c00-2c1481730111",
                "Tristan und Isolde (1981)":"https://d279gtpur1viyb.cloudfront.net/A05005284/66753db7-18ac-43e6-90dc-9871d0e119be",
                "Der Freischütz (2017)":"https://d279gtpur1viyb.cloudfront.net/O815317/b82eb1df-c7be-4b62-a09a-dc17b8c1d149",
                "Der Freischütz (2018)":"https://d279gtpur1viyb.cloudfront.net/A04050091/7bd2334f-05b8-433b-8b3f-2a5ced67160c",
                "Die Passagierin":"https://d279gtpur1viyb.cloudfront.net/A04001538/22fb4ce0-c876-4b1e-b486-67a3693277ac",
                "Das Labyrinth - Der Zauberflöte zweiter Tehil":"https://d279gtpur1viyb.cloudfront.net/A04001580/92504034-0859-48fd-8b6c-a46367ba5351",
                "Der Vogelhändler":"https://d279gtpur1viyb.cloudfront.net/O815997/e9e3daa5-0be7-4f2b-a34f-2149334ce7d7"
}
'''
data = json.loads(jsondb)
keys = data.keys()
headers = []
aud_quality = {
        '128 kbps':'1_stereo_128000',
        '360 kbps':'1_stereo_360000',
        '640 kbps':'1_stereo_640000'
        }
aud_quality_man = ['128 kbps','360 kbps','640 kbps']
vid_quality = { 
        '144p (190 kbps)':'144_190464',
        '288p (381 kbps)':'288_380928',
        '360p (688 kbps)':'360_688128',
        '432p (1098 kbps)':'432_1097728',
        '576p (1405 kbps)':'576_1404928',
        'HD 720p (2288 kbps)':'720_2287616',
        'Full HD 1080p (3113 kbps)':'1080_3112960'
        }
vid_quality_man = ['144p (190 kbps)','288p (381 kbps)','360p (688 kbps)','432p (1098 kbps)','576p (1405 kbps)','HD 720p (2288 kbps)','Full HD 1080p (3113 kbps)']
for key in sorted(keys):
        headers.append(key)

layout = [  [sg.Text('Opera name:'),sg.Text('                    Audio resolution:'),sg.Text('Video resolution:')],
            [sg.Combo(headers,size=(30,1),key = 'st_name'), sg.Combo(aud_quality_man,size=(10,1),key='aud_quality'), sg.Text(' '), sg.Combo(vid_quality_man,size=(20,1),key='vid_quality')],
            [sg.Text('Select download location:'),sg.In(key='save_path'),sg.FolderBrowse()],
            [sg.Output(size=(80,20))],
            [sg.Text('Progress:'),sg.Text('0% (0 of 0)     ',key='progress_percent'),sg.ProgressBar(100,orientation='h',size=(30,20), bar_color=('chartreuse2','white'), key='Progress')],
            [sg.Button('Start'), sg.Button('Close')] ]
            
window = sg.Window('Stream Downloader',layout)
total_pb = window['Progress']
pc = window['progress_percent']

while True:
        global event,values
        event,values = window.read()
        if event == 'Close' or event == sg.WIN_CLOSED:
                break
        elif event == 'Start':
                path = values['save_path']
                if path == '':
                        if os.path.exists('Download'):
                                pass
                        else:

                                os.mkdir('Download')
                        path = './Download'
                else:
                        os.chdir(path)
                #if os.path.exists('Download'):
                #       pass
                #else:

                #       os.mkdir('Download')
                #os.chdir('Download')
                name = values['st_name']
                
                try:
                        os.mkdir(name)
                        #shutil.rmtree('temp')
                except Exception:
                        pass
                
                os.chdir(name)
                shutil.rmtree('./temp', ignore_errors=True)
                os.mkdir('temp')
                os.chdir('temp')
                audq = aud_quality.get(values['aud_quality'])
                vidq = vid_quality.get(values['vid_quality'])
                src = data.get(name)
                global down
                down = threading.Thread(target=Sources.MyFidelio.Silent,args=(src,audq,vidq,total_pb,pc),daemon=True)
                down.start()
                #break

                check = threading.Thread(target=Check)
                check.start()

                try:
                        done
                except Exception:
                        pass
                else:
                        print('Procesing - merging audio and video.')
                        ff = FFmpeg(
                        inputs={'video.mp4': None, 'audio.mp4': None},
                        outputs={'../../'+name+'.mp4': '-c:v copy -c:a aac -loglevel quiet'}
                        )
                        ff.run()
                        os.chdir('../..')
                        shutil.rmtree(name)
                        print('Finished downloading '+name+', You can now go ahead and download more or close the program.')
                        print('')
                        print('')
                        print('Enjoy!')
                        print('')
                        print('Thanks for using my software.')
