# assignment 01
from __future__ import print_function
from pyclausie import ClausIE
# re
import re
re_spaces = re.compile(r'\s+') # Create RegEx object looking for strings?
# spacy
import spacy
nlp = spacy.load('en') # Loads the english model

class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        """
        :param name: the person's name
        :type name: basestring
        :param likes: (Optional) an initial list of likes
        :type likes: list
        :param dislikes: (Optional) an initial list of likes
        :type dislikes: list
        :param has: (Optional) an initial list of things the person has
        :type has: list
        :param travels: (Optional) an initial list of the person's travels
        :type travels: list
        """
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels
    def __repr__(self):
        return self.name
    def addPet(self, petType, petName=None):
        for index in range(len(self.has)):
            if str(type(self.has[index])) == "<class 'Pet'>" and self.has[index].type == petType:
                if (self.has[index].name is None) and (petName != None):
                    pet = name_pet(petType, petName)
                    # self.has[index].name = petName
                    self.has[index] = pet
                return self.has[index]
        pet = add_pet(petType, petName)
        self.has.append(pet)
        return pet




class Pet(object):
    def __init__(self, pet_type, name=None):
        self.name = name
        self.type = pet_type
    def __repr__(self):
        if(self.name == None):
            return self.type
        else:
            return self.type + ": " + self.name

class Trip(object):
    def __init__(self):
        self.departs_on = None
        self.departs_to = None
    def __repr__(self):
        return self.departs_to

# initialize persons, pets, trips lists
persons = []
pets = []
trips = []

# Data input function
def process_data_from_input_file(file_path = 'Assignment_01/assignment_01.data'): #infile = open("./assignment_01.data")
    """
    :param file_path: path from which to read the input data
    :type file_path: string path to .txt or .data file
    :return: cleaned lines from input file
    :rtype: list
    """
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not (line.startswith(('$$$', '###', '===')) or line =="\n")]
    return cleaned_lines
# Answer retrieval functions
def select_person(name): #Selects a person from the list
    for person in persons:
        if person.name == name:
            return person
def add_person(name): #Adds a person to the list, returns it
    person = select_person(name)
    if person is None:
        new_person = Person(name)
        persons.append(new_person)
        return new_person
    return person
def select_pet(name): #Selects a pet from the list
    for pet in pets:
        if pet.name == name:
            return pet
def add_pet(type, name=None): #Adds a new pet to the list, returns it
    pet = None
    if name:
        pet = select_pet(name)
    if pet is None:
        pet = Pet(type, name)
        pets.append(pet)
    return pet
def name_pet(type, name): #Renames a previously unnamed pet of a certain type
    for index in range(len(pets)):
        if pets[index].type == type and pets[index].name is None:
            pets[index].name = name
            return pets[index]
def get_persons_pets(person_name): #Selects a persons' pet from the list
    person = select_person(person_name)
    for thing in person.has:
        return [thing for thing in person.has if isinstance(thing, Pet)]
def get_persons_dog(person_name):
    person_pets = get_persons_pets(person_name)
    if person_pets and [animal for animal in person_pets if animal.type == 'dog']:
        return [animal for animal in person_pets if animal.type == 'dog'][0]
def get_persons_cat(person_name):
    person_pets = get_persons_pets(person_name)
    if person_pets and [animal for animal in person_pets if animal.type == 'cat']:
        return [animal for animal in person_pets if animal.type == 'cat'][0]
# def get_persons_pet(person_name): #Selects a persons' pet from the list
#     person = select_person(person_name)
#     for thing in person.has:
#         if isinstance(thing, Pet):
#             return thing
def get_persons_destinations(person_name):
    person = select_person(person_name)
    for thing in

# Relation triplet
def process_relation_triplet(triplet):
    """
    Process a relation triplet found by ClausIE and store the data
    find relations of types:
    (PERSON, likes, PERSON)
    (PERSON, has, PET) #done
    (PET, has_name, NAME)
    (PERSON, travels, TRIP)
    (TRIP, departs_on, DATE)
    (TRIP, departs_to, PLACE)

    :param triplet: The relation triplet from ClausIE
    :type triplet: tuple
    :return: a triplet in the formats specified above
    :rtype: tuple
    """
    #triplet = cl.extract_triples(["Bob has a dog named Fido."])[0]
    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object
    doc = nlp(unicode(sentence))
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
        # elif t.pos_ == 'NOUN'
    # also, if only one sentence # root = doc[:].root
    """
    CURRENT ASSUMPTIONS:
    - People's names are unique (i.e. there only exists one person with a certain name).
    - Pet's names are unique
    - The only pets are dogs and cats
    - Only one person can own a specific pet
    - A person can own only one pet
    """
    subj_span = doc.char_span(sentence.find(triplet.subject), len(triplet.subject)) #Sentence subject span
    obj_span = doc.char_span(sentence.find(triplet.object), len(sentence)) #Sentence object span
    # Process (PERSON, likes, PERSON) relations
    if root.lemma_ == 'like':
        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and triplet.object in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(triplet.object)
            s.likes.append(o)

    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        fw_doc = nlp(unicode(triplet.object))
        with_token = [t for t in fw_doc if t.text == 'with'][0]
        fw_who = [t for t in with_token.children if t.dep_ == 'pobj'][0].text
        # fw_who = [e for e in fw_doc.ents if e.label_ == 'PERSON'][0].text

        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and fw_who in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(fw_who)
            s.likes.append(o)
            o.likes.append(s)

    # Process (PET.name)
    if root.lemma_ == 'be' and 'name' in triplet.subject and ('dog' in triplet.subject or 'cat' in triplet.subject):
        pet_type = 'dog' if 'dog' in triplet.subject else 'cat' #is it a dog or a cat?
        person_name = [word.text for word in subj_span if word.pos_ == 'PROPN'][0]
        person = add_person(person_name)
        # pet_name = triplet.object
        pet_name = ' '.join([word.text for word in obj_span if word.pos_ == 'PROPN']) # MAYBE REMOVE THIS, MRS. BINGLESWORTH
        person.addPet(petType = pet_type, petName = pet_name)
    # Process (PERSON, has, PET)
    if root.lemma_ == 'have' and ('dog' in triplet.object or 'cat' in triplet.object): #################################3
        pet_type = 'dog' if 'dog' in triplet.object else 'cat' #is it a dog or a cat?
        person = add_person(triplet.subject) #################
        if any([word.pos_ == 'PROPN' for word in obj_span]):
            #[n if obj_span[n].pos_ == 'PROPN' for n in range(len(obj_span))]
            pet_name = [word.text for word in obj_span if word.pos_ == 'PROPN'][0]
            person.addPet(petType = pet_type, petName = str(pet_name))
            # pet = add_pet(pet_type, name = str(pet_name))
            # person.has.append(pet)
        else: #no name given
            person.addPet(pet_type)
            # pet = add_pet(pet_type)
            # person.has.append(pet)
    # Process (PET, has, NAME)
    if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject): #this one isnt mine
        obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))

        # handle single names, but what about compound names? Noun chunks might help.
        if len(obj_span) == 1 and obj_span[0].pos_ == 'PROPN':
            name = triplet.object
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

            s_people = [token.text for token in subj_doc if token.ent_type_ == 'PERSON']
            assert len(s_people) == 1
            s_person = add_person(s_people[0]) #was: select_person

            s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'

            pet = add_pet(s_pet_type, name)
            person.addPet(petType = s_pet_type, petName = str(name))

            # s_person.has.append(pet)

    # Process (PERSON, travels, TRIP)
    if root.lemma_ in ['go', 'fly'] and
    # Process (TRIP, departs_on, DATE)
    # Process (TRIP, departs_to, PLACE)

def preprocess_question(question):
    # remove articles: a, an, the
    q_words = question.split(' ')
    # when won't this work?
    for article in ('a', 'an', 'the'): #Removes each of these
        try:
            q_words.remove(article)
        except:
            pass
    return re.sub(re_spaces, ' ', ' '.join(q_words))
def has_question_word(string): # Returns True if the string has a question word
    # note: there are other question words
    for qword in ('who', 'what', 'does', 'when'): #('who', 'what')
        if qword in string.lower():
            return True
    return False
# Data setup and processing
def load_data():
    input_data = process_data_from_input_file()  # get input data
    cl = ClausIE.get_instance()  # setup the NLP thing
    triples = cl.extract_triples(input_data)  # turn the input data into some triples
    return cl, triples
def process_data(raw_triples):
    for t in raw_triples:
        try: r = process_relation_triplet(t)
        except: pass

#Main function!
def answer_question(question): #this is key
    # Turn question into a triple
    q_trip = cl.extract_triples([preprocess_question(question)])[0]
    sentence = q_trip.subject + ' ' + q_trip.predicate + ' ' + q_trip.object
    doc = nlp(unicode(sentence))
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
    # Answers for different questions:
    # (WHO, has, PET)
    if q_trip.subject.lower() == 'who' and root.lemma_ == 'have': #DONE!
        answer = '{} has a {} named {}.'
        if q_trip.object == 'dog':
            for person in persons:
                pet = get_persons_dog(person.name)
                if pet:
                    print(answer.format(person.name, 'dog', pet.name))
        elif q_trip.object == 'cat':
            for person in persons:
                pet = get_persons_cat(person.name)
                if pet:
                    print(answer.format(person.name, 'cat', pet.name))
    # (WHO, going to, PLACE)
    if q_trip.subject.lower() == 'who' and root.lemma_ in ['go', 'fly']:
        answer = '{} ' + q_trip.predicate + ' ' + q_trip.object
        for
        print(answer.format(NAMEHERE, root, ))

    answer = 'answer' #wtf is this
    return answer

#main()
def main():
    # input_data = process_data_from_input_file() #get input data
    # cl = ClausIE.get_instance() #setup the NLP thing
    # triples = cl.extract_triples(input_data) #turn the input data into some triples
    # for t in triples:
    #     try: r = process_relation_triplet(t)
    #     except: pass
    cl, triples = load_data()
    process_data(triples)

    question = ' '
    while question[-1] != '?':
        question = raw_input("Please enter your question: ")
        if question[-1] != '?':
            print('This is not a question... please try again')
    answer_question(question)
    return 1

#__main__ function \/ \/
# if __name__ == '__main__':
#    main()
#__main__ function /\ /\
def check_pets():
    print(persons)
    for person in persons:
        print(person, end = ":")
        pet = get_persons_pets(person.name)
        print(pet, end = "; ")
        print(person.has)
def check_span(theSpan):
    for word in theSpan:
        print(word, end = ": ")
        print(word.pos_)
def setup_test(): #15, 8
    triplet = triples[17]  # Joe 's cat 's name is Mr. Binglesworth
    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object
    doc = nlp(unicode(sentence))
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
    subj_span = doc.char_span(sentence.find(triplet.subject), len(triplet.subject))  # Sentence subject span
    obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))  # Sentence object span
"""
Helpful data: 

question = "Who is traveling to Japan?"

for word in doc: 
    print(word, end = ": ")
    print(word.pos_, end = ", ") #PROPN, 
    print(word.head, end = ", ")) #? 
    print()

"""
#TODO: REMOVE!!!
cl, triples = load_data()
process_data(triples)
"""
Functions useful for testing: 
dir(object)

Doc objects made up of Token objects (words)
Doc object: 
doc.ents 

Token objects: 
word.pos_ #PROPN, VERB, ADJ, NOUN, ADP
word.head_
word.text

ALT-Shift-E: Run selected code in Python Console 
"""