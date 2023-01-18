# TEE PELI TÄHÄN
#Väistele haamuja ja kerää kolikoita. F2 aloittaa uuden pelin. Oven kuva jäi nyt käyttämättä.
#Haamut syntyvät ruudun ulkopuolella. Kolikot saattavat syntyä myös pelaajan kohdalle suoraan ja poimittaessa siirretään ruudun ulkopuolelle.
import pygame, random
class Hirvio:
    def __init__(self):
        if random.randint(0, 1): #randomoidaan alku x
            self.x = -100 + random.randint(0, 50)
        else:
            self.x = random.randint(800, 850)
        if random.randint(0, 1): #randomoidaan alku y
            self.y = -100 + random.randint(0, 50)
        else:
            self.y = random.randint(800, 850)
        #self.y = random.randint(0, 530)
        if random.randint(0,1): #randomoidaan hirviön syntymäliikesuunta
            self.xnopeus = 1
            self.ynopeus = 2
        else:
            self.xnopeus = -2
            self.ynopeus = -1
    
    def liiku(self):
        self.x += self.xnopeus
        if self.x + 50 >= 900 and self.xnopeus > 0:
            self.xnopeus = -self.xnopeus
        if self.x <= -100 and self.xnopeus < 0:
            self.xnopeus = -self.xnopeus
        
        self.y += self.ynopeus
        if self.y + 70 >= 900 and self.ynopeus > 0:
            self.ynopeus = -self.ynopeus
        if self.y <= -100 and self.ynopeus < 0:
            self.ynopeus = -self.ynopeus

class Pelaaja:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.xnopeus = 4
        self.ynopeus = 4
    
class Kolikko:
    def __init__(self):
        self.x = random.randint(0, 760)
        self.y = random.randint(0, 560)

class Ovi:
    def __init__(self):
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 530)


class Peli:
    def __init__(self):
        pygame.init()
        
        self.lataa_kuvat()
        self.uusi_peli()
        self.pelaajan_liikkuminen()

        #self.korkeus = len(self.kartta)
        #self.leveys = len(self.kartta[0])
        #self.skaala = self.kuvat[0].get_width()
        self.kello = pygame.time.Clock()

        nayton_korkeus = 800
        nayton_leveys = 800
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))

        self.fontti = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("DC:n hieno väistelypeli, jossa kerätään kolikoita")

        self.silmukka()

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["robo", "kolikko", "hirvio", "ovi"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
        
        self.robo = self.kuvat[0]
        self.kolikko = self.kuvat[1]
        self.hirvio = self.kuvat[2]
        #self.ovi = self.kuvat[3]

    def uusi_peli(self):
        self.pisteet = 0
        self.hirviot = [Hirvio()]
        self.pelaaja = Pelaaja()
        self.kolikot = [Kolikko()]
        #self.ovi = Ovi()
        self.aika = 0
        self.osumat = 0
    
    def pelaajan_liikkuminen(self):
        self.vasemmalle = False
        self.oikealle = False
        self.ylos = False
        self.alas = False

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
                
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
            
        if self.oikealle:
            if self.pelaaja.x <= 800 - self.robo.get_width():
                self.pelaaja.x += 2
        if self.vasemmalle:
            if self.pelaaja.x >= 0:
                self.pelaaja.x -= 2
        if self.ylos:
            if self.pelaaja.y >= 0:
                self.pelaaja.y -= 2
        if self.alas:
            if self.pelaaja.y <= 800 - self.robo.get_height():
                self.pelaaja.y += 2

    def piirra_naytto(self):
        self.naytto.fill((255, 255, 255))

        self.naytto.blit(self.kuvat[0], (self.pelaaja.x, self.pelaaja.y))
        for kolikko in self.kolikot:
            self.naytto.blit(self.kuvat[1], (kolikko.x, kolikko.y))
            if kolikko.x < self.pelaaja.x and self.pelaaja.x < kolikko.x + 40 or kolikko.x > self.pelaaja.x and self.pelaaja.x + 40 > kolikko.x:# vasen ja oikea kosketus kolikkoon
                if kolikko.y < self.pelaaja.y and self.pelaaja.y < kolikko.y + 40 or kolikko.y > self.pelaaja.y and self.pelaaja.y + 80 > kolikko.y: # yläkosketus, alakosketus kolikkoon
                    self.pisteet += 1
                    kolikko.x, kolikko.y = -111, -111
        
        #self.naytto.blit(self.kuvat[3], (self.ovi.x, self.ovi.y))
        for hirvio in self.hirviot:
            self.naytto.blit(self.kuvat[2], (hirvio.x, hirvio.y))
            hirvio.liiku()
            if hirvio.x < self.pelaaja.x and self.pelaaja.x < hirvio.x + 40 or hirvio.x > self.pelaaja.x and self.pelaaja.x + 40 > hirvio.x:# vasen ja oikea kosketus hirviöön
                if hirvio.y < self.pelaaja.y and self.pelaaja.y < hirvio.y + 80 or hirvio.y > self.pelaaja.y and self.pelaaja.y + 80 > hirvio.y: # yläkosketus, alakosketus hirviöön
                    self.osumat += 1

        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (0, 0, 0))
        self.naytto.blit(teksti, (370, 770))
        teksti = self.fontti.render("Osumat: " + str(self.osumat), True, (0, 0, 0))
        self.naytto.blit(teksti, (370, 740))
        teksti = self.fontti.render("Esc = sulje peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (20, 770))
        teksti = self.fontti.render("F2 = uusi peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (650, 770))

        pygame.display.flip()
        self.aika += 1
        if self.aika % 360 == 0:
            self.hirviot.append(Hirvio()) #lisätään hirvio 6 sekunnin välein
        if self.aika % 180 == 0:
            self.kolikot.append(Kolikko()) #lisätään kolikko 3 sekunnin välein
        self.kello.tick(60)

if __name__ == "__main__":
    Peli()