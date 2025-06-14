Τεχνητή Νοημοσύνη

Εργασία 2 Απαντήσεις

Ονοματεπώνυμο: Κυριάκος Λάμπρος Κιουράνας
Α.Μ.: 1115201900238

### Question 1

Σε αυτή την ερωτημα υλοποίησα ένα Reflex Agent που λαμβάνει αποφάσεις με βάση την τρέχουσα κατάσταση του παιχνιδιού, προσπαθώντας να βελτιώσει το σκορ του. Ο στόχος ήταν να φτιάξω έναν agent που λαμβάνει υπόψη τις τοποθεσίες τροφής και φαντασμάτων.

- Για εκτελεση:
  
```bash
python pacman.py -p ReflexAgent -l testClassic
```

Δοκίμασα επίσης το layout `mediumClassic` με ένα ή δύο φαντάσματα:

```bash
python pacman.py --frameTime 0 -p ReflexAgent -k 1
python pacman.py --frameTime 0 -p ReflexAgent -k 2
```

### Question 2

Σε αυτή την ερωτημα υλοποίησα έναν agent Minimax, ο οποίος λαμβάνει αποφάσεις με στόχο τη μεγιστοποίηση του σκορ του Pacman και την ελαχιστοποίηση της απόδοσης των φαντασμάτων.

- Για εκτελεση:

```bash
python autograder.py -q q2
```

Χωρίς γραφικά:

```bash
python autograder.py -q q2 --no-graphics
```

### Question 3

Σε αυτή την ερωτημα, βελτίωσα την απόδοση του Minimax Agent, χρησιμοποιώντας τον αλγόριθμο Alpha-Beta Pruning. Ο στόχος ήταν η αποδοτική εξερεύνηση του δέντρου αποφάσεων.

- Για εκτελεση:

```bash
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```

### Question 4

Σε αυτή την ερωτημα, υλοποίησα τον Expectimax Agent, ο οποίος λαμβάνει υπόψη τη στοχαστική συμπεριφορά των φαντασμάτων. Σε αντίθεση με τον Minimax, ο Expectimax δεν υποθέτει ότι τα φαντάσματα δρουν βέλτιστα.

- Για εκτελεση:

```bash
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```

### Question 5

Στην τελική ερώτηση, βελτίωσα τη συνάρτηση αξιολόγησης, ώστε ο Pacman να μπορεί να λαμβάνει καλύτερες αποφάσεις. Η συνάρτηση αυτή αξιολογεί καταστάσεις, λαμβάνοντας υπόψη την απόσταση από την τροφή, τα φαντάσματα και τα power pellets.

- Για εκτελεση:

```bash
python autograder.py -q q5
```

Χωρίς γραφικά:

```bash
python autograder.py -q q5 --no-graphics
```
