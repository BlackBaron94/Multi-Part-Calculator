<a id="readme-top"></a>
<div align="center">
  <h1 align="center">Multi-Part Calculator</h1>

  <p align="center">
    Ένα script που υπολογίζει μαθηματικές παραστάσεις με όλες τις βασικές πράξεις, παρενθέσεις!
    </p>
</div>

## Περιεχόμενα
- [Περιγραφή Project](#περιγραφή-project)
- [Οδηγίες Εγκατάστασης](#οδηγίες-εγκατάστασης)
- [Λειτουργίες](#λειτουργίες)
- [Χρήση](#χρήση)
- [Μελλοντικές Προσθήκες](#μελλοντικές-προσθήκες)
- [Επικοινωνία](#επικοινωνία)

## Περιγραφή Project 

Το script είναι χωρίς UI, δέχεται από τον χρήστη μαθηματική παράσταση σε console και την υπολογίζει! 
Δουλεύει υπολογίζοντας με βάσει την σειρά προτεραιότητας των πράξεων και παρενθέσεων. Υποστηρίζει όλες
τις βασικές πράξεις μεταξύ ακεραίων και δεκαδικών.

### Τεχνολογίες και βιβλιοθήκες που χρησιμοποιήθηκαν

* [![Python][python.org]][Python-url]
* [![RegEx][RegEx-Icon]][RegEx-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Οδηγίες Εγκατάστασης


1. Clone του repo
   ```sh
   git clone https://github.com/BlackBaron94/Multi-Part-Calculator.git
   ```

Για να τρέξει το αρχείο .py χρειάζεται εγκατεστημένη έκδοση 3. Python.

2. Έλεγχος εγκατεστημένης έκδοσης Python
   ```sh
   python --version
   ```
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Λειτουργίες

Η εφαρμογή μπορεί να εκτελέσει όλες τις παρακάτω πράξεις μεταξύ ακεραίων και δεκαδικών, θετικών
και αρνητικών αριθμών:

1. ***Πρόσθεση*** με το σύμβολο +
2. ***Αφαίρεση*** με το σύμβολο -
3. ***Πολλαπλασιασμό*** με το σύμβολο *
4. ***Διαίρεση*** με το σύμβολο /
5. ***Ύψωση σε δύναμη*** με το σύμβολο ^
6. ***Πράξεις με αρνητικούς αριθμούς*** βάζοντας τους σε παρένθεση
7. ***Υπολογισμό προσήμων*** βάζοντας τα σε παρένθεση πριν τον αριθμό
8. ***Πράξεις με παρενθέσεις*** χωρίς ανάγκη χρήσης αγκυλών για εμφωλευμένες παρενθέσεις

Η εφαρμογή εντοπίζει σφάλματα εισαγωγής δεδομένων και τα προλαμβάνει με αμυντικό προγραμματισμό, 
για παράδειγμα τα κενά αγνοούνται, μη επιτρεπόμενα σύμβολα και γράμματα εντοπίζονται, λάθη στην
εισαγωγή εντοπίζονται εγκαίρως και διευκρινίζουν το λάθος που εντοπίστηκε.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Χρήση

Το script δέχεται παραστάσεις με προσημασμένους αριθμούς μόνο σε παρενθέσεις, για παράδειγμα:
- 3*-5 αυτό δεν είναι σωστό, καθώς απαιτεί παρένθεση
- 3*(-5) αυτό όμως θα υπολογιστεί σωστά!
---------
- 2+-5 αυτό δεν είναι σωστό, καθώς απαιτεί παρενθέσεις
- 2+(-5) αυτό θα υπολογιστεί σωστά!
---------
Οι πράξεις αλληλουχίας χωρίς ρητά διατυπωμένη (με παρενθέσεις) προτεραιότητα γίνονται από τα αριστερά προς τα δεξιά,
δηλαδή:
- 56/7/2 = (56/7)/2 = 8/2 = 4 και όχι 56/(7/2) = 56/3.5 = 16
- 2^2^3 = (2^2)^3 = 4^3 = 64 και όχι 2^(2^3) = 2^8 = 256
---------
Η διαίρεση προηγείται του πολλαπλασιασμού, δηλαδή:
- 56/7\*2 = (56/7)\*2 = 8\*2 = 16 και όχι 56/(7\*2) = 56/14 = 4
---------
Για πολλαπλασιασμό δηλώνεται ρητά η πράξη με το σύμβολο * και δεν υποννοείται ποτέ, δηλαδή:
- 3+5(2+2) αυτό θα βγάλει μήνυμα λάθους που ζητάει σύμβολο πράξης
- 3+5*(2+2) αυτό είναι σωστό και θα υπολογιστεί σωστά!
--------
Οι παρενθέσεις δε χρειάζεται να μπούνε σε σειρά προτεραίοτητας με [] και {}, το πρόγραμμα μετατρέπει όλα τα είδη
σε παρενθέσεις και λύνει με αυτές! Μπορείτε να τις χρησιμοποιείτε όπως θέλετε, αρκεί να κλείνουν όλες, δηλαδή:
- {20/\[4*(4+1)]} = {20/(4*\[4+1))) = (20/(4*(4+1))) και τα τρία υπολογίζονται σωστά από το πρόγραμμα
- (20/(4*(4+1) αυτό όμως θα οδηγήσει σε σφάλμα επειδή δεν κλείνουν σωστά οι παρενθέσεις,
όπως τονίζει και το αντίστοιχο μήνυμα που επιστρέφει το πρόγραμμα
-------
Μπορείτε να χρησιμοποιείτε είτε , είτε . για κατάδειξη δεκαδικών ψηφίων το πρόγραμμα θα το εντοπίσει σωστά!
- 2.5+2,5 θα δώσει σωστά αποτέλεσμα 5
-------
Παρακάτω ακολουθούν διάφορα παραδείγματα σωστής λειτουργίας του script.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Μελλοντικές Προσθήκες

- [X] Προσθήκη πράξης ύψωσης σε δύναμη.
- [X] Προσθήκη υπολογισμού παρενθέσεων.
- [X] Προσθήκη υπολογισμού αλληλουχίας προσήμων. 
- [ ] Προσθήκη πράξης modulo (MOD).
- [ ] Προσθήκη πράξης ακέραιας διαίρεσης (DIV).
- [ ] Προσθήκη UI.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Επικοινωνία

Γιώργος Τσολακίδης - [Linked In: Giorgos Tsolakidis](https://www.linkedin.com/in/black-baron/) - black_baron94@hotmail.com 

Project Link: [Multi-Part Calculator](https://github.com/BlackBaron94/Multi-Part-Calculator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://python.org/
[RegEx-Icon]: https://raw.githubusercontent.com/BlackBaron94/images/main/RegexLogo.png
[RegEx-url]: https://regexr.com/
