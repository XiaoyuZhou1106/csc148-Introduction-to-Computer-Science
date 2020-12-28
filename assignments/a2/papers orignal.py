"""Assignment 2: Modelling CS Education research paper data

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.

TODO: (Task 6) Complete the steps below
Recommended steps:
1. Start by reviewing the provided dataset in cs1_papers.csv. You can assume
   that any data used to generate this tree has this format,
   i.e., a csv file with the same columns (same column names, same order).
   The categories are all in one column, separated by colons (':').
   However, you should not make assumptions about what the categories are, how
   many categories there are, the maximum number of categories a paper can have,
   or the number of lines in the file.

2. Read through all the docstrings in this file once. There is a lot to take in,
   so don't feel like you need to understand it all the first time.
   Draw some pictures!
   We have provided the headers of the initializer as well as of some helper
   functions we suggest you implement. Note that we will not test any
   private top-level functions, so you can choose not to implement these
   functions, and you can add others if you want to for your solution.
   For this task, we will be testing that you are building the correct tree,
   not that you are doing it in a particular way. We will access your class
   in the same way as in the client code in the visualizer.

3. Plan out what you'll need to do to implement the PaperTree initializer.
   In particular, think about how to use the boolean parameters to do different
   things in setting up the tree. You may also find it helpful to review the
   Python documentation about the csv module, which you are permitted and
   encouraged to use. You should have a good plan, including what your subtasks
   are, before you begin writing any code.

4. Write the code for the PaperTree initializer and any helper functions you
   want to use in your design. You should not make any changes to the public
   interface of this module, or of the PaperTree class, but you can add private
   attributes and helpers as needed.

5. Tidy and test your code, and try it with the visualizer client code. Make
   sure you have documented any new private attributes, and that PyTA passes
   on your code.
"""
import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    TODO: Add any of your new private attributes here.
    _author:
        The author of the paper.
    _doi:
        The doi address of the paper.
    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - All TMTree RIs are inherited.
    """
    _author: str
    _doi: str

    # TODO: Add the type contracts for your new attributes here

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        TMTree.__init__(self, self.rect, self._colour, self._name, self._subtrees, self._parent_tree, self._expanded)
        # self._name = name
        # self._subtrees = subtrees
        if all_papers:
            self._subtrees = _build_tree_from_dict(_load_papers_to_dict(\
                by_year))
        # self.rect = (0, 0, 0, 0)
        # self._parent_tree = None
        # self._expanded = False
        # self._colour = (random.randint(0, 255), random.randint(0, 255), \
        #                 random.randint(0, 255))
        # for a in self._subtrees:
        #     a._parent_tree = self
        self._author = authors
        self._doi = doi
        self.data_size = 0
        if self._subtrees == []:
            self.data_size = citations
        else:
            for sub in self._subtrees:
                self.data_size += sub.data_size
        if self.data_size == 0:


        # TODO: Complete this initializer. Your implementation must not
        # TODO: duplicate anything done in the superclass initializer.

def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    #TODO: Implement this helper, or remove it if you do not plan to use it
    result = {}
    reader = csv.DictReader(open(DATA_FILE))
    if by_year:
        for row in reader:
        lst = row['Category'].strip().split(': ')
        lst.append(row['Title'])
        author = row['Author']
        url = row['Url']
        citation = int(row['Citations'])
        dct = {'Author': author, 'Url': url, 'Citations': citation}
        lst.append(dct)
        if row['Year'] not in result:
            result[row['Year']] = {}
        _load_list_to_dic(lst, result[row['Year']])
    else:
        for row in reader:
        lst = row['Category'].strip().split(': ')
        lst.append(row['Title'])
        _load_list_to_dic(lst, result)
    return result


def _load_list_to_dic(l: List, d: Dict) -> None:
    """balbla"""
    if l[0] in d:
        if len(l) >= 3:
            new = l[1:]
            _load_list_to_dic(new, d[l[0]])
    else:
        d[l[0]] = {}
        for k in reversed(l[1:]):
            d[l[0]] = {k: d[l[0]]}

#Author, Title, Year, Category, Url, Citations


def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    # TODO: Implement this helper, or remove it if you do not plan to use it
    result = []
    for key in nested_dict:
        if 'Author' in nested_dict[key] and 'Url' in nested_dict[key]:
            # reader = csv.DictReader(open(DATA_FILE))
            # for row in reader:
            #     if key == row['Title']:
            author = nested_dict[key]['Author']
            url = nested_dict[key]['Url']
            citation = int(nested_dict[key]['Citations'])
            y = PaperTree(key, [], author, url, citation, True, False)
            result.append(y)
        else:
            sub = _build_tree_from_dict(nested_dict[key])
            v = PaperTree(key, sub, '', '', 0, True, False)
            result.append(v)

    return result


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
# "Salton, Gerard",Introductory Programming at Cornell,1973,Students: non-majors,http://doi.acm.org/10.1145/800010.808068,3
# "Gries, David",What Should We Teach in an Introductory Programming Course?,1974,FLP: other: language agnostic approaches,http://doi.acm.org/10.1145/800183.810447,32
# "Conway, Richard W.",Introductory Instruction in Programming,1974,Students: other: enrollment issues,http://doi.acm.org/10.1145/800183.810430,3
# "Shapiro, Stuart C. and Witmer, Douglas P.",Interactive Visual Simulators for Beginning Programming Students,1974,Tools: editors apis etc,http://doi.acm.org/10.1145/800183.810431,5
# "Danielson, Ronald L. and Nievergelt, Jurg",An Automatic Tutor for Introductory Programming Students,1975,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/800284.811129,2
# "Cherniak, Bob",Introductory Programming Reconsidered - a User-oriented Approach,1976,DSA: general,http://doi.acm.org/10.1145/800107.803449,6
# "Ecklund,Jr., E. F.",A Ldquo;Non-programming\&Rdquo; Introduction to Programming Concepts,1976,FLP: other: language agnostic approaches,http://doi.acm.org/10.1145/800107.803448,0
# "Brewer, Richard K.",Documentation Standards for Beginning Students,1976,Teaching: other: focus on documentation or requirements or specifications or design,http://doi.acm.org/10.1145/800107.803450,1
# "Shneiderman, Ben","Evaluating Introductory Programming Textbooks: A Guide for Students, Instructors, Authors and Publishers",1977,Content: other: textbook choice,http://doi.acm.org/10.1145/800106.803434,0
# "Alford, M. and Hsia, P. and Petry, F.",A Software Engineering Approach to Introductory Programming Courses,1977,Content: software engineering approaches,http://doi.acm.org/10.1145/800104.803381,3
# "Oldehoeft, R. R. and Roman, R. V.",Methodology for Teaching Introductory Computer Science,1977,DSA: general,http://doi.acm.org/10.1145/800104.803373,1
# "Hosch, Frederick A.",Whither Flowcharting?,1977,Teaching: other: flowcharting,http://doi.acm.org/10.1145/800106.803437,2
# "Schneider, G. Michael",The Introductory Programming Course in Computer Science: Ten Principles,1978,DSA: general,http://doi.acm.org/10.1145/990555.990598,14
# "Bowles, Kenneth L.",A CS1 Course Based on Stand-alone Microcomputers,1978,DSA: other,http://doi.acm.org/10.1145/990555.990601,7
# "Epley, Donald and Sjoerdsma, Ted",A Two-semester Course Sequence in Introductory Programming Using PL/1\&Mdash;a Rationale and Overview,1978,FLP: other: language migration,http://doi.acm.org/10.1145/800130.804244,3
# "Furuta, Richard and Kemp, P. Michael",Experimental Evaluation of Programming Language Features: Implications for Introductory Programming Languages,1979,FLP: general,http://doi.acm.org/10.1145/800126.809544,0
# "Kimura, Takayuki",Reading Before Composition,1979,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/800126.809575,3
# "Mitchell, William",Another Approach to Service Courses,1979,Students: non-majors,http://doi.acm.org/10.1145/800126.809541,2
# "Ellison, Robert J.",A Programming Sequence for the Liberal Arts College,1980,DSA PS: other,http://doi.acm.org/10.1145/800140.804628,1
# "Kurtz, Barry L.",Investigating the Relationship Between the Development of Abstract Reasoning and Performance in an Introductory Programming Class,1980,Students: predicting and measuring success,http://doi.acm.org/10.1145/800140.804622,9
# "Harrison, Warren A. and Magel, Kenneth I.",A Suggested Course in Introductory Computer Programming,1981,DSA: general,http://doi.acm.org/10.1145/800037.800961,2
# "Smith, Jeffrey W.",A Method for Teaching Programming,1981,Teaching: general,http://doi.acm.org/10.1145/800037.800996,1
# "Tharp, Alan L.",Getting More Oomph from Programming Exercises,1981,Teaching: model problems and examples,http://doi.acm.org/10.1145/800037.800968,3
# "Richards, Thomas C.",Cost Effective Methods for Teaching Introductory Programming Courses,1982,DSA: other,http://doi.acm.org/10.1145/800066.801353,2
# "Shub, Charles M.",Does the Computer System Make a Difference in the Effectiveness of the Introductory Service Course?,1982,DSA: other,http://doi.acm.org/10.1145/800066.801341,1
# "Olson, Lynn J.",A Lab Approach for Introductory Programming Courses,1983,DSA PS: labs,http://doi.acm.org/10.1145/800038.801039,3
# "Barker, Ricky J. and Unger, E. A.",A Predictor for Success in an Introductory Programming Class Based Upon Abstract Reasoning Development,1983,Students: predicting and measuring success,http://doi.acm.org/10.1145/800038.801037,11
# "Mazlack, Lawrence J.",Introducing Subprograms As the First Control Structure in an Introductory Course,1983,Teaching: aids examples tricks,http://doi.acm.org/10.1145/800038.801062,3
# "Levine, Liz and Woolf, Beverly and Filoramo, Rich",Do I Press Return?,1984,Students: retention,http://doi.acm.org/10.1145/800039.808642,3
# "Fox, Christopher and Lancaster, Ronald L.",Use of a Syntax Checker to Improve Student Access to Computing,1984,Tools: debugging and testing,http://doi.acm.org/10.1145/800039.808624,0
# "McGlinn, Robert J. and Lewis, Linda","IPEX1, a Library of Dynamic Introductory Programming Examples",1985,Teaching: model problems and examples,http://doi.acm.org/10.1145/323287.323291,0
# "Stokes, Gordon E. and Christensen, Larry C. and Hays, Bill",ELROND: A Computer Based Instruction System for an Introductory Programming Course,1985,Teaching: other,http://doi.acm.org/10.1145/323287.323293,2
# "Tam, Wing C. and Erlinger, Michael A.",On the Teaching of Ada in an Undergraduate Computer Science Curriculum,1987,FLP: specific text-based languages,http://doi.acm.org/10.1145/31820.31734,4
# "Wilson, Judith D.",A Socratic Approach to Helping Novice Programmers Debug Programs,1987,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/31820.31755,2
# "Lukey, Trevor and Loose, Kenneth and Hill, David R.",Implementation of a Debugging Aid for Logic Errors in Pascal Programs,1987,Tools: debugging and testing,http://doi.acm.org/10.1145/31820.31792,2
# "Means, H. Willis",A Content Analysis of Ten Introduction to Programming Textbooks,1988,Content: other: textbook choice,http://doi.acm.org/10.1145/52964.53035,1
# "Pattis, Richard E.",Textbook Errors in Binary Searching,1988,Content: other: textbook choice,http://doi.acm.org/10.1145/52964.53012,4
# "Deneen, Linda L. and Pierce, Keith R.",Development and Documentation of Computer Programs in Undergraduate Computer Science Programs,1988,Content: software engineering approaches,http://doi.acm.org/10.1145/52964.52970,3
# "Koffman, Elliot B.",The Case for Modula-2 in CS1 and CS2,1988,FLP: specific text-based languages,http://doi.acm.org/10.1145/52964.52978,5
# "Liss, Ivan B. and McMillan, Thomas C.",An Amazing Exercise in Recursion for CS1 and CS2,1988,Teaching: model problems and examples,http://doi.acm.org/10.1145/52964.53032,6
# "Brown, Dale A.","Requiring CS1 Students to Write Requirements Specifications: A Rationale, Implementation Suggestions, and a Case Study",1988,Teaching: other: focus on documentation or requirements or specifications or design,http://doi.acm.org/10.1145/52964.52969,7
# "Pratt, Terrence W.",Teaching Programming: A New Approach Based on Analysis Skills,1988,Teaching: other: problem solving first,http://doi.acm.org/10.1145/52964.53026,5
# "Mitchell, William",What is to Become of Programming?,1989,DSA: dealing with ACM model curricula,http://doi.acm.org/10.1145/65293.65306,1
# "Luker, P. A.","Never Mind the Language, What About the Paradigm?",1989,FLP: specific paradigms,http://doi.acm.org/10.1145/65293.71442,8
# "Winslow, L. E. and Lang, J. E.",Ada in CS1,1989,FLP: specific text-based languages,http://doi.acm.org/10.1145/65293.71215,5
# "Waguespack,Jr., Leslie J.",Visual Metaphors for Teaching Programming Concepts,1989,Teaching: aids examples tricks,http://doi.acm.org/10.1145/65293.71203,8
# "Liss, Ivan B. and McMillan, Thomas C.","An Example Illustrating Modularity, Abstraction \&Amp; Information Hiding Using",1989,Teaching: model problems and examples,http://doi.acm.org/10.1145/65293.71195,1
# "Schweitzer, Dino and Teel, Scott C.",AIDE: An Automated Tool for Teaching Design in an Introductory Programming Course,1989,Tools: other,http://doi.acm.org/10.1145/65293.71202,0
# "Joyce, Daniel T.",A Virtual Lab to Accompany CS1 and CS2,1990,DSA PS: labs,http://doi.acm.org/10.1145/323410.319077,6
# "Pratt, Terrence W.",Upgrading CS1: An Alternative to the Proposed COCS Survey Course,1990,DSA: dealing with ACM model curricula,http://doi.acm.org/10.1145/323410.319086,6
# "Pattis, Richard E.",A Philosophy and Example of CS-1 Programming Projects,1990,Teaching: model problems and examples,http://doi.acm.org/10.1145/323410.319076,17
# "Chavey, Darrah",A Structured Laboratory Component for the Introductory Programming Course,1991,DSA PS: labs,http://doi.acm.org/10.1145/107004.107067,10
# "Katz, Elizabeth E. and Porter, Hayden S.",HyperTalk As an Overture to CS1,1991,FLP: specific text-based languages,http://doi.acm.org/10.1145/107004.107015,1
# "Bailie, Frances K.",Improving the Modularization Ability of Novice Programmers,1991,Teaching: other: problem solving first,http://doi.acm.org/10.1145/107004.107065,1
# "Alvarez Rubio, Juan",A First Computing Course Based on Curricula 1991,1992,DSA: dealing with ACM model curricula,http://doi.acm.org/10.1145/134510.134512,1
# "Baldwin, Doug and Koomen, Johannes A. G. M.",Using Scientific Experiments in Early Computer Science Laboratories,1992,LA: assessment: authentic assessment,http://doi.acm.org/10.1145/134510.134532,22
# "Tam, Wing C.",Teaching Loop Invariants to Beginners by Examples,1992,Teaching: aids examples tricks,http://doi.acm.org/10.1145/134510.134530,5
# "Lang, Joseph E. and Smith, Barbara A.",Scheduled Supervised Laboratories in CS1: A Comparative Analysis,1993,DSA PS: labs,http://doi.acm.org/10.1145/169070.169397,5
# "Fekete, Alan",Reasoning About Programs: Integrating Verification and Analysis of Algorithms into the Introductory Programming Course,1993,DSA: dealing with ACM model curricula,http://doi.acm.org/10.1145/169070.169410,2
# "Dyck, V. Arnie",Emphasizing the Process in Delivering CS-1,1993,DSA: general,http://doi.acm.org/10.1145/169070.169363,0
# "Decker, Rick and Hirshfield, Stuart",Top-down Teaching: Object-oriented Programming in CS 1,1993,FLP: specific paradigms,http://doi.acm.org/10.1145/169070.169495,13
# "Reid, Richard J.",The Object Oriented Paradigm in CS 1,1993,FLP: specific paradigms,http://doi.acm.org/10.1145/169070.169491,12
# "Pattis, Richard E.",The \&Ldquo;Procedures Early\&Rdquo; Approach in CS 1: A Heresy,1993,FLP: specific paradigms,http://doi.acm.org/10.1145/169070.169362,16
# "Roberts, Eric S.",Using C in CS1: Evaluating the Stanford Experience,1993,FLP: specific text-based languages,http://doi.acm.org/10.1145/169070.169361,22
# "Carmony, Lowell A. and Holliday, Robert L.",An Example from Artificial Intelligence for CS1,1993,Teaching: aids examples tricks,http://doi.acm.org/10.1145/169070.169077,2
# "Sabin, Roberta Evans and Sabin, Edward P.",Collaborative Learning in an Introductory Computer Science Course,1994,CA: other,http://doi.acm.org/10.1145/191029.191156,9
# "Gersting, Judith L.",A Software Engineering \&Ldquo;Frosting\&Rdquo; on a Traditional CS-1 Course,1994,Content: software engineering approaches,http://doi.acm.org/10.1145/191029.191129,9
# "Zachary, Joseph L.",Tutorial-based Teaching of Introductory Programming Classes,1994,DSA PS: labs,http://doi.acm.org/10.1145/191029.191085,4
# "Waller, William A.",A Framework for CS1 and CS2 Laboratories,1994,DSA PS: labs,http://doi.acm.org/10.1145/191029.191107,4
# "Oliver, S. Ron and Dalbey, John",A Software Development Process Laboratory for CS1 and CS2,1994,DSA PS: labs,http://doi.acm.org/10.1145/191029.191097,13
# "Thweatt, Mack",CSI Closed Lab vs. Open Lab Experiment,1994,DSA PS: labs,http://doi.acm.org/10.1145/191029.191064,19
# "Meter, Glenn and Miller, Philip","Engaging Students and Teaching Modern Concepts: Literate, Situated, Object-oriented Programming",1994,DSA: general,http://doi.acm.org/10.1145/191029.191161,4
# "Decker, Rick and Hirshfield, Stuart",The Top 10 Reasons Why Object-oriented Programming Can'T Be Taught in CS 1,1994,FLP: specific paradigms,http://doi.acm.org/10.1145/191029.191054,28
# "Pattis, Richard E.",Teaching EBNF First in CS 1,1994,Teaching: aids examples tricks,http://doi.acm.org/10.1145/191029.191155,4
# "Calloni, Ben A. and Bagert, Donald J.",ICONIC Programming in BACCII vs. Textual Programming: Which is a Better Learning Environment?,1994,Tools: visualization,http://doi.acm.org/10.1145/191029.191103,9
# "Astrachan, Owen and Reed, David",AAA and CS 1: The Applied Apprenticeship Approach to CS 1,1995,CA: other,http://doi.acm.org/10.1145/199688.199694,24
# "Parker, David L.",Structured Design for CS1,1995,Content: software engineering approaches,http://doi.acm.org/10.1145/199688.199810,3
# "Willshire, Mary Jane","Old Dogs, New Tricks",1995,FLP: specific paradigms,http://doi.acm.org/10.1145/199688.199771,1
# "Wick, Michael R.",On Using C++ and Object-orientation in CS1: The Message is Still More Important Than the Medium,1995,FLP: specific text-based languages,http://doi.acm.org/10.1145/199688.199840,6
# "Herrmann, Nira and Popyack, Jeffrey L.",Creating an Authentic Learning Experience in Introductory Programming Courses,1995,LA: assessment: authentic assessment,http://doi.acm.org/10.1145/199688.199780,6
# "Schorsch, Tom","CAP: An Automated Self-assessment Tool to Check Pascal Programs for Syntax, Logic and Style Errors",1995,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/199688.199769,17
# "Roberts, Eric and Lilly, John and Rollins, Bryan",Using Undergraduates As Teaching Assistants in Introductory Programming Courses: An Update on the Stanford Experience,1995,Teaching: other: teaching assistants and mentors,http://doi.acm.org/10.1145/199688.199716,25
# "Roberts, Eric S.",Loop Exits and Structured Programming: Reopening the Debate,1995,Teaching: specific topics (arrays recursion etc),http://doi.acm.org/10.1145/199688.199815,7
# "Roberts, Eric S.",A C-based Graphics Library for CS1,1995,Tools: libraries etc,http://doi.acm.org/10.1145/199688.199767,21
# "Fekete, Alan and Greening, Antony",Designing Closed Laboratories for a Computer Science Course,1996,DSA PS: labs,http://doi.acm.org/10.1145/236452.236559,6
# "McGill, Tanya and Hobbs, Valerie",A Supplementary Package for Distance Education Students Studying Introductory Programming,1996,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/236452.236512,1
# "Adams, Joel C.",Object-centered Design: A Five-phase Introduction to Object-oriented Programming in CS1\&Ndash;2,1996,FLP: specific paradigms,http://doi.acm.org/10.1145/236452.236513,2
# "K\""{o}lling, Michael and Rosenberg, John",Blue\&Mdash;a Language for Teaching Object-oriented Programming,1996,FLP: specific text-based languages,http://doi.acm.org/10.1145/236452.236537,19
# "Bareiss, Catherine C.",A Semester Project for CS1,1996,Teaching: model problems and examples,http://doi.acm.org/10.1145/236452.236562,7
# "Barrett, Martin L.",Emphasizing Design in CS1,1996,Teaching: other: focus on documentation or requirements or specifications or design,http://doi.acm.org/10.1145/236452.236563,4
# "Walker, Henry M.",Collaborative Learning: A Case Study for CS1 at Grinnell College and Austin,1997,CA: other,http://doi.acm.org/10.1145/268084.268164,19
# "Holmes, Goefrey and Smith, Tony C.",Adding Some Spice to CS1 Curricula,1997,Content: other: breadth-first or depth-first CS1,http://doi.acm.org/10.1145/268084.268163,9
# "Hilburn, Thomas B. and Towhidnejad, Massood",Doing Quality Work: The Role of Software Process Definition in the Computer Science Curriculum,1997,Content: software engineering approaches,http://doi.acm.org/10.1145/268084.268193,7
# "Pargas, Roy P. and Lundy, Joe C. and Underwood, John N.",Tournament Play in CS1,1997,Teaching: model problems and examples,http://doi.acm.org/10.1145/268084.268166,8
# "Fell, Harriet J. and Proulx, Viera K.",Exploring Martian Planetary Images: C++ Exercises for CS1,1997,Teaching: model problems and examples,http://doi.acm.org/10.1145/268084.268093,21
# "Zachary, Joseph L.","The Gestalt of Scientific Programming: Problem, Model, Method, Implementation, Assessment",1997,Teaching: model problems and examples,http://doi.acm.org/10.1145/268084.268173,4
# "Nebash, Bohdan and Feldman, Michael B.",Using HTML Linking to Help Novice Programmers to Reuse Components,1997,Teaching: other,http://doi.acm.org/10.1145/268084.268204,0
# "Schulze, Kay G. and Grodzinsky, Frances S.",Teaching Ethical and Social Issues in CS1 and CS2,1997,Teaching: other: ethical and societal issues,http://doi.acm.org/10.1145/268084.268087,2
# "Hou, Lily and Tomayko, James",Applying the Personal Software Process in CS1: An Experiment,1998,Content: software engineering approaches,http://doi.acm.org/10.1145/273133.274322,3
# "Tjaden, Bunny J.",Do Lab Modules in CS Actually Help Students?: An Empirical Study,1998,DSA PS: labs,http://doi.acm.org/10.1145/273133.274313,0
# "Mercuri, Rebecca and Herrmann, Nira and Popyack, Jeffrey",Using HTML and JavaScript in Introductory Programming Courses,1998,FLP: specific text-based languages,http://doi.acm.org/10.1145/273133.273754,10
# "Wu, Cheng-Chih and Dale, Nell B. and Bethel, Lowell J.",Conceptual Models and Cognitive Learning Styles in Teaching Recursion,1998,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/273133.274315,24
# "Adams, Joel C.",Chance-It: An Object-oriented Capstone Project for CS-1,1998,Teaching: model problems and examples,http://doi.acm.org/10.1145/273133.273140,20
# "Astrachan, Owen and Rodger, Susan H.","Animation, Visualization, and Interaction in CS 1 Assignments",1998,Teaching: model problems and examples,http://doi.acm.org/10.1145/273133.274321,27
# "Reed, David",Incorporating Problem-solving Patterns in CS1,1998,Teaching: other: problem solving first,http://doi.acm.org/10.1145/273133.273137,7
# "Sangwan, Raghvinder S. and Korsh, James F. and LaFollette,Jr., Paul S.",A System for Program Visualization in the Classroom,1998,Tools: visualization,http://doi.acm.org/10.1145/273133.274311,6
# "Carrasquel, Jacobo","Teaching CS1 On-line: The Good, the Bad, and the Ugly",1999,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/299649.299758,6
# "Woodworth, Pat and Dann, Wanda",Integrating Console and Event-driven Models in CS1,1999,FLP: specific paradigms,http://doi.acm.org/10.1145/299649.299720,7
# "Ginat, David and Shifroni, Eyal",Teaching Recursion in a Procedural Environment\&Mdash;How Much Should We Emphasize the Computing Model?,1999,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/299649.299718,21
# "Stone, Don C. and Bergmann, Seth and Baliga, Ganesh and Berman, A. Michael and Schmalzel, John","A CS1 Maze Lab, Using Joysticks and MIPPETs",1999,Teaching: model problems and examples,http://doi.acm.org/10.1145/299649.299743,4
# "Jim{\'e}nez-Peris, Ricardo and Khuri, Sami and Pati\~{n}o-Mart\'{\i}nez, Marta",Adding Breadth to CS1 and CS2 Courses Through Visual and Interactive Programming Projects,1999,Teaching: model problems and examples,http://doi.acm.org/10.1145/299649.299774,18
# "Ziegler, Uta and Crews, Thad",An Integrated Program Development Tool for Teaching and Learning How to Program,1999,Tools: editors apis etc,http://doi.acm.org/10.1145/299649.299786,8
# "Warford, J. Stanley",BlackBox: A New Object-oriented Framework for CS1/CS2,1999,Tools: editors apis etc,http://doi.acm.org/10.1145/299649.299785,4
# "Cheatham, Thomas J.",A Web-based Lab Manual for CS 1: An Experiment,2000,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/330908.331828,0
# "Lewis, John",Myths About Object-orientation and Its Pedagogy,2000,FLP: specific paradigms,http://doi.acm.org/10.1145/330908.331863,14
# "Vandenberg, Scott and Wollowski, Michael",Introducing Computer Science Using a Breadth-first Approach and Functional Programming,2000,FLP: specific paradigms,http://doi.acm.org/10.1145/330908.331851,7
# "Reges, Stuart",Conservatively Radical Java in CS1,2000,FLP: specific text-based languages,http://doi.acm.org/10.1145/330908.331821,17
# "Buck, Duane and Stucki, David J.",Design Early Considered Harmful: Graduated Exposure to Complexity and Structure Based on Levels of Cognitive Development,2000,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/330908.331817,43
# "George, Carlisle E.",EROSI\&Mdash;Visualising Recursion and Discovering New Errors,2000,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/330908.331875,15
# "Tesser, Herbert and Al-Haddad, Hisham and Anderson, Gary",Instrumentation: A Multi-science Integrated Sequence,2000,Teaching: aids examples tricks,http://doi.acm.org/10.1145/330908.331861,3
# "Wick, Michael R.",Kaleidoscope: Using Design Patterns in CS1,2001,Content: upper level topics in CS1,http://doi.acm.org/10.1145/364447.364596,6
# "Lischner, Ray",Explorations: Structured Labs for First-time Programmers,2001,DSA PS: labs,http://doi.acm.org/10.1145/364447.364571,10
# "Preston, Jon A. and Wilson, Laura",Offering CS1 On-line Reducing Campus Resource Demand While Improving the Learning Environment,2001,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/364447.364618,4
# "Veal, D. and Maj, S. P. and Duley, Rick",Assessing \&Ldquo;Hands on\&Rdquo; Skills on CS1 Computer \&Amp; Network Technology Units,2001,LA: assessment: authentic assessment,http://doi.acm.org/10.1145/364447.364751,0
# "Lister, Raymond",Objectives and Objective Assessment in CS1,2001,LA: assessment: general,http://doi.acm.org/10.1145/364447.364605,20
# "Odekirk-Hash, Elizabeth and Zachary, Joseph L.",Automated Feedback on Programs Means Students Need Less Help from Teachers,2001,LA: assessment: other: automatic feedback and/or grading,http://doi.acm.org/10.1145/364447.364537,13
# "Wilson, Brenda Cantwell and Shrock, Sharon",Contributing to Success in an Introductory Computer Science Course: A Study of Twelve Factors,2001,Students: predicting and measuring success,http://doi.acm.org/10.1145/364447.364581,116
# "Applin, Anne Gates",Second Language Acquisition and CS1,2001,Teaching: aids examples tricks,http://doi.acm.org/10.1145/364447.364579,4
# "Buck, Duane and Stucki, David J.",JKarelRobot: A Case Study in Supporting Levels of Cognitive Development in the Computer Science Curriculum,2001,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/364447.364529,27
# "Becker, Byron Weber",Teaching CS1 with Karel the Robot in Java,2001,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/364447.364536,25
# "Wolz, Ursula",Teaching Design and Project Management with Lego RCX Robots,2001,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/364447.364551,19
# "Gegg-Harrison, Timothy S.",Ancient Egyptian Numbers: A CS-complete Example,2001,Teaching: model problems and examples,http://doi.acm.org/10.1145/364447.364598,2
# "Anderson, Richard and Dickey, Martin and Perkins, Hal",Experiences with Tutored Video Instruction for Introductory Programming Courses,2001,Teaching: video,http://doi.acm.org/10.1145/364447.364619,5
# "Bruce, Kim B. and Danyluk, Andrea and Murtagh, Thomas",A Library to Support a Graphics-based Object-first Approach to CS 1,2001,Tools: libraries etc,http://doi.acm.org/10.1145/364447.364527,29
# "Koffman, Elliot and Wolz, Ursula",A Simple Java Package for GUI-like Interactivity,2001,Tools: libraries etc,http://doi.acm.org/10.1145/364447.364528,6
# "McDowell, Charlie and Werner, Linda and Bullock, Heather and Fernald, Julian",The Effects of Pair-programming on Performance in an Introductory Programming Course,2002,CA: pair programming,http://doi.acm.org/10.1145/563340.563353,103
# "Vasiga, Troy",What Comes After CS 1 + 2: A Deep Breadth Before Specializing,2002,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/563340.563350,1
# "Roumani, Hamzeh",Design Guidelines for the Lab Component of Objects-first CS1,2002,FLP: specific paradigms,http://doi.acm.org/10.1145/563340.563426,14
# "Califf, Mary Elaine and Goodwin, Mary",Testing Skills and Knowledge: Introducing a Laboratory Exam in CS1,2002,LA: assessment: exams,http://doi.acm.org/10.1145/563340.563425,9
# "Thomas, Lynda and Ratcliffe, Mark and Woodbury, John and Jarman, Emma",Learning Styles and Performance in the Introductory Programming Sequence,2002,LA: learning: learning styles,http://doi.acm.org/10.1145/563340.563352,44
# "Comer, James and Roggio, Robert",Teaching a Java-based CS1 Course in an Academically-diverse Environment,2002,Students: non-majors,http://doi.acm.org/10.1145/563340.563396,4
# "Barnes, David J.",Teaching Introductory Java Through LEGO MINDSTORMS Models,2002,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/563340.563397,21
# "Thomas, Lynda and Ratcliffe, Mark and Robertson, Ann",Code Warriors and Code-a-phobes: A Study in Attitude and Pair Programming,2003,CA: pair programming,http://doi.acm.org/10.1145/611892.612007,37
# "Nagappan, Nachiappan and Williams, Laurie and Ferzli, Miriam and Wiebe, Eric and Yang, Kai and Miller, Carol and Balik, Suzanne",Improving the CS1 Experience with Pair Programming,2003,CA: pair programming,http://doi.acm.org/10.1145/611892.612006,90
# "Adams, Joel and Frens, Jeremy",Object Centered Design for Java: Teaching OOD in CS-1,2003,Content: upper level topics in CS1,http://doi.acm.org/10.1145/611892.611986,5
# "Clancy, Michael and Titterton, Nate and Ryan, Clint and Slotta, Jim and Linn, Marcia","New Roles for Students, Instructors, and Computers in a Lab-based Introductory Programming Course",2003,DSA PS: labs,http://doi.acm.org/10.1145/611892.611951,8
# "Woit, Denise and Mason, David",Effectiveness of Online Assessment,2003,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/611892.611952,18
# "Herrmann, Nira and Popyack, Jeffrey L. and Char, Bruce and Zoski, Paul and Cera, Christopher D. and Lass, Robert N. and Nanjappa, Aparna",Redesigning Introductory Computer Programming Using Multi-level Online Modules for a Mixed Audience,2003,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/611892.611967,11
# "Phillips, Andrew T. and Stevenson, Daniel E. and Wick, Michael R.",Implementing CC2001: A Breadth-first Introductory Course for a Just-in-time Curriculum Design,2003,DSA: dealing with ACM model curricula,http://doi.acm.org/10.1145/611892.611978,9
# "Powers, Kris D.",Breadth-also: A Rationale and Implementation,2003,DSA: dealing with ACM model curricula,http://doi.acm.org/10.1145/611892.611979,5
# "Cooper, Stephen and Dann, Wanda and Pausch, Randy",Teaching Objects-first in Introductory Computer Science,2003,FLP: specific paradigms,http://doi.acm.org/10.1145/611892.611966,121
# "Sanders, Dean and Dorn, Brian",Jeroo: A Tool for Introducing Object-oriented Programming,2003,FLP: specific text-based languages,http://doi.acm.org/10.1145/611892.611968,26
# "Lister, Raymond and Leaney, John","Introductory Programming, Criterion-referencing, and Bloom",2003,LA: assessment: general,http://doi.acm.org/10.1145/611892.611954,38
# "Hristova, Maria and Misra, Ananya and Rutter, Megan and Mercuri, Rebecca",Identifying and Correcting Java Programming Errors for Introductory Computer Science Students,2003,LA: learning: errors,http://doi.acm.org/10.1145/611892.611956,44
# "Lane, H. Chad and VanLehn, Kurt",Coached Program Planning: Dialogue-based Support for Novice Program Design,2003,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/611892.611955,12
# "Shannon, Christine",Another Breadth-first Approach to CS I Using Python,2003,Students: non-majors,http://doi.acm.org/10.1145/611892.611980,23
# "Giguette, Ray",Pre-games: Games Designed to Introduce CS1 and CS2 Programming Assignments,2003,Teaching: aids examples tricks,http://doi.acm.org/10.1145/611892.611990,15
# "Fagin, Barry and Merkle, Laurence",Measuring the Effectiveness of Robots in Teaching Computer Science,2003,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/611892.611994,29
# "Burger, Kevin R.",Teaching Two-dimensional Array Concepts in Java with Image Processing Examples,2003,Teaching: model problems and examples,http://doi.acm.org/10.1145/611892.611970,15
# "Bouvier, Dennis J.",Pilot Study: Living Flowcharts in an Introduction to Programming Course,2003,Teaching: other: flowcharting,http://doi.acm.org/10.1145/611892.611991,2
# "Reges, Stuart",Using Undergraduates As Teaching Assistants at a State University,2003,Teaching: other: teaching assistants and mentors,http://doi.acm.org/10.1145/611892.611943,12
# "Lucas, Jeff and Naps, Thomas L. and R\""{o}\ssling, Guido",VisualGraph: A Graph Class Designed for Both Undergraduate Students and Educators,2003,Tools: visualization,http://doi.acm.org/10.1145/611892.611960,5
# "Burch, Carl and Ziegler, Lynn",Science of Computing Suite (SOCS): Resources for a Breadth-first Introduction,2004,Content: other: breadth-first or depth-first CS1,http://doi.acm.org/10.1145/971300.971447,5
# "Herrmann, Nira and Popyack, Jeffrey L. and Char, Bruce and Zoski, Paul",Assessment of a Course Redesign: Introductory Computer Programming Using Online Modules,2004,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/971300.971326,6
# "Roberts, Eric",The Dream of a Common Language: The Search for Simplicity and Stability in Computer Science Education,2004,FLP: general,http://doi.acm.org/10.1145/971300.971343,14
# "DePasquale, Peter and Lee, John A. N. and P{\'e}rez-Qui\~{n}ones, Manuel A.",Evaluation of Subsetting Programming Language Elements in a Novice's Programming Environment,2004,FLP: other: language subsets,http://doi.acm.org/10.1145/971300.971392,3
# "Bennedsen, Jens and Caspersen, Michael E.",Programming in Context: A Model-first Approach to CS1,2004,FLP: specific paradigms,http://doi.acm.org/10.1145/971300.971461,16
# "Howe, Emily and Thornton, Matthew and Weide, Bruce W.",Components-first Approaches to CS1/CS2: Principles and Practice,2004,FLP: specific paradigms,http://doi.acm.org/10.1145/971300.971404,8
# "Frens, Jeremy D.",Taming the Tiger: Teaching the Next Version of Java,2004,FLP: specific text-based languages,http://doi.acm.org/10.1145/971300.971356,2
# "Mahmoud, Qusay H. and Dobosiewicz, Wlodek and Swayne, David","Redesigning Introductory Computer Programming with HTML, JavaScript, and Java",2004,FLP: specific text-based languages,http://doi.acm.org/10.1145/971300.971344,8
# "Daly, Charlie and Waldron, John",Assessing the Assessment of Programming Ability,2004,LA: assessment: general,http://doi.acm.org/10.1145/971300.971375,15
# "Edwards, Stephen H.",Using Software Testing to Move Students from Trial-and-error to Reflection-in-action,2004,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/971300.971312,75
# "Chmiel, Ryan and Loui, Michael C.",Debugging: From Novice to Expert,2004,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/971300.971310,15
# "Rich, Lauren and Perry, Heather and Guzdial, Mark",A CS1 Course Designed to Address Interests of Women,2004,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/971300.971370,73
# "Moskal, Barbara and Lurie, Deborah and Cooper, Stephen",Evaluating the Effectiveness of a New Instructional Approach,2004,Students: other: (attitudes self-efficacy at-risk),http://doi.acm.org/10.1145/971300.971328,91
# "McKinney, Dawn and Denton, Leo F.","Houston, We Have a Problem: There's a Leak in the CS1 Affective Oxygen Tank",2004,Students: predicting and measuring success,http://doi.acm.org/10.1145/971300.971386,19
# "Ventura, Phil and Ramamurthy, Bina",Wanted: CS1 Students. No Experience Required,2004,Students: prior knowledge,http://doi.acm.org/10.1145/971300.971387,20
# "Holliday, Mark A. and Luginbuhl, David",CS1 Assessment Using Memory Diagrams,2004,Teaching: aids examples tricks,http://doi.acm.org/10.1145/971300.971373,6
# "K\""{o}lling, Michael and Barnes, David J.",Enhancing Apprentice-based Learning of Java,2004,Teaching: general,http://doi.acm.org/10.1145/971300.971403,12
# "Reed, Dale and John, Sam and Aviles, Ryan and Hsu, Feihong",CFX: Finding Just the Right Examples for CS1,2004,Teaching: model problems and examples,http://doi.acm.org/10.1145/971300.971426,1
# "Etheredge, Jim",CMeRun: Program Logic Debugging Courseware for CS1/CS2 Students,2004,Tools: debugging and testing,http://doi.acm.org/10.1145/971300.971311,7
# "Proulx, Viera K. and Rasala, Richard",Java IO and Testing Made Simple,2004,Tools: debugging and testing,http://doi.acm.org/10.1145/971300.971358,3
# "Reis, Charles and Cartwright, Robert",Taming a Professional IDE for the Classroom,2004,Tools: editors apis etc,http://doi.acm.org/10.1145/971300.971357,7
# "Lewis, Tracy L. and Rosson, Mary Beth and P{\'e}rez-Qui\~{n}ones, Manuel A.",What Do the Experts Say?: Teaching Introductory Design from an Expert's Perspective,2004,Tools: other,http://doi.acm.org/10.1145/971300.971405,11
# "Beck, Leland L. and Chizhik, Alexander W. and McElroy, Amy C.",Cooperative Learning Techniques in CS1: Design and Experimental Evaluation,2005,CA: other,http://doi.acm.org/10.1145/1047344.1047495,19
# "Trytten, Deborah A.",A Design for Team Peer Code Review,2005,CA: other,http://doi.acm.org/10.1145/1047344.1047492,18
# "Tew, Allison Elliott and Fowler, Charles and Guzdial, Mark",Tracking an Innovation in Introductory CS Education from a Research University to a Two-year College,2005,Content: other: media computation,http://doi.acm.org/10.1145/1047344.1047481,29
# "McKinney, Dawn and Denton, Leo F.","Affective Assessment of Team Skills in Agile CS1 Labs: The Good, the Bad, and the Ugly",2005,Content: software engineering approaches,http://doi.acm.org/10.1145/1047344.1047494,7
# "Dougherty, John P. and Wonnacott, David G.",Use and Assessment of a Rigorous Approach to CS1,2005,Content: upper level topics in CS1,http://doi.acm.org/10.1145/1047344.1047431,2
# "Wick, Michael R.",Teaching Design Patterns in CS1: A Closed Laboratory Sequence Based on the Game of Life,2005,Content: upper level topics in CS1,http://doi.acm.org/10.1145/1047344.1047499,6
# "Soh, Leen-Kiat and Samal, Ashok and Person, Suzette and Nugent, Gwen and Lang, Jeff",Closed Laboratories with Embedded Instructional Research Design for CS1,2005,DSA PS: labs,http://doi.acm.org/10.1145/1047344.1047448,5
# "Dierbach, Charles and Taylor, Blair and Zhou, Harry and Zimand, Iliana",Experiences with a CS0 Course Targeted for CS1 Success,2005,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/1047344.1047453,10
# "Hsia, James I. and Simpson, Elspeth and Smith, Daniel and Cartwright, Robert",Taming Java for the Classroom,2005,FLP: specific text-based languages,http://doi.acm.org/10.1145/1047344.1047459,7
# "Traynor, Des and Gibson, J. Paul",Synthesis and Analysis of Automatic Assessment Methods in CS1: Generating Intelligent MCQs,2005,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/1047344.1047502,6
# "Cohen, Robert F. and Fairley, Alexander V. and Gerry, David and Lima, Gustavo R.",Accessibility in Introductory Computer Science,2005,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/1047344.1047367,11
# "Guzdial, Mark and Forte, Andrea",Design Process for a Non-majors Computing Course,2005,Students: non-majors,http://doi.acm.org/10.1145/1047344.1047468,40
# "Lane, H. Chad and VanLehn, Kurt",Intention-based Scoring: An Approach to Measuring Success at Solving the Composition Problem,2005,Students: predicting and measuring success,http://doi.acm.org/10.1145/1047344.1047471,5
# "Bergin, Susan and Reilly, Ronan",Programming: Factors That Influence Success,2005,Students: predicting and measuring success,http://doi.acm.org/10.1145/1047344.1047480,50
# "Soh, Leen-Kiat and Samal, Ashok and Person, Suzette and Nugent, Gwen and Lang, Jeff","Designing, Implementing, and Analyzing a Placement Test for Introductory CS Courses",2005,Students: prior knowledge,http://doi.acm.org/10.1145/1047344.1047504,1
# "Stevenson, Daniel E. and Wick, Michael R. and Ratering, Steven J.","Steganography and Cartography: Interesting Assignments That Reinforce Machine Representation, Bit Manipulation, and Discrete Structures Concepts",2005,Teaching: model problems and examples,http://doi.acm.org/10.1145/1047344.1047443,4
# "Wicentowski, Richard and Newhall, Tia",Using Image Processing Projects to Teach CS1 Topics,2005,Teaching: model problems and examples,http://doi.acm.org/10.1145/1047344.1047445,14
# "Califf, Mary Elaine and Goodwin, Mary",Effective Incorporation of Ethics into Courses That Focus on Programming,2005,Teaching: other: ethical and societal issues,http://doi.acm.org/10.1145/1047344.1047464,4
# "Daly, Charlie and Horgan, Jane",Patterns of Plagiarism,2005,Teaching: other: plagiarism,http://doi.acm.org/10.1145/1047344.1047473,9
# "Bruce, Kim B. and Danyluk, Andrea and Murtagh, Thomas",Why Structural Recursion Should Be Taught Before Arrays in CS 1,2005,Teaching: specific topics (arrays recursion etc),http://doi.acm.org/10.1145/1047344.1047430,6
# "Bennedsen, Jens and Caspersen, Michael E.",Revealing the Programming Process,2005,Teaching: video,http://doi.acm.org/10.1145/1047344.1047413,19
# "Gonzalez, Graciela",A Systematic Approach to Active and Cooperative Learning in CS1 and Its Effects on CS2,2006,CA: other,http://doi.acm.org/10.1145/1121341.1121386,22
# "McKinney, Dawn and Denton, Leo F.",Developing Collaborative Skills Early in the CS Curriculum in a Laboratory Environment,2006,CA: other,http://doi.acm.org/10.1145/1121341.1121387,19
# "Pedroni, Michela and Meyer, Bertrand",The Inverted Curriculum in Practice,2006,Content: other: media computation,http://doi.acm.org/10.1145/1121341.1121493,14
# "Bower, Matt",Virtual Classroom Pedagogy,2006,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/1121341.1121390,8
# "Roumani, Hamzeh",Practice What You Preach: Full Separation of Concerns in CS1/CS2,2006,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/1121341.1121495,5
# "Chen, Tzu-Yi and Monge, Alvaro and Simon, Beth",Relationship of Early Programming Language to Novice Generated Design,2006,FLP: general,http://doi.acm.org/10.1145/1121341.1121496,3
# "Reges, Stuart",Back to Basics in CS1 and CS2,2006,FLP: specific paradigms,http://doi.acm.org/10.1145/1121341.1121432,34
# "Soh, Leen-Kiat",Incorporating an Intelligent Tutoring System into CS1,2006,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/1121341.1121494,4
# "Roberts, Eric",An Interactive Tutorial System for Java,2006,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/1121341.1121447,2
# "Peterson, Laurence I. and Benham, Dale",Overview of the cyberTech-ITEST Project: An Initiative to Attract and Prepare Under-represented Students for Tomorrow's Careers in the Computing Sciences,2006,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/1121341.1121480,1
# "Bayliss, Jessica D. and Strout, Sean","Games As a ""Flavor"" of CS1",2006,Teaching: games,http://doi.acm.org/10.1145/1121341.1121498,55
# "Bierre, Kevin and Ventura, Phil and Phelps, Andrew and Egert, Christopher",Motivating OOP by Blowing Things Up: An Exercise in Cooperation and Competition in an Introductory Java Programming Course,2006,Teaching: model problems and examples,http://doi.acm.org/10.1145/1121341.1121452,19
# "DePasquale, Peter",Exploiting On-line Data Sources As the Basis of Programming Projects,2006,Teaching: model problems and examples,http://doi.acm.org/10.1145/1121341.1121430,7
# "Decker, Adrienne and Ventura, Phil and Egert, Christopher",Through the Looking Glass: Reflections on Using Undergraduate Teaching Assistants in CS1,2006,Teaching: other: teaching assistants and mentors,http://doi.acm.org/10.1145/1121341.1121358,8
# "Byckling, Pauli and Sajaniemi, Jorma",Roles of Variables and Programming Skills Improvement,2006,Teaching: specific topics (arrays recursion etc),http://doi.acm.org/10.1145/1121341.1121470,14
# "Janzen, David S. and Saiedian, Hossein",Test-driven Learning: Intrinsic Integration of Testing into the CS/SE Curriculum,2006,Tools: debugging and testing,http://doi.acm.org/10.1145/1121341.1121419,32
# "Bower, Matt",Groupwork Activities in Synchronous Online Classroom Spaces,2007,CA: other,http://doi.acm.org/10.1145/1227310.1227345,4
# "Murtagh, Thomas P.",Weaving CS into CS1: A Doubly Depth-first Approach,2007,Content: other: breadth-first or depth-first CS1,http://doi.acm.org/10.1145/1227310.1227429,9
# "Clifton, Curtis and Kaczmarczyk, Lisa C. and Mrozek, Michael",Subverting the Fundamentals Sequence: Using Version Control to Enhance Course Management,2007,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/1227310.1227344,8
# "Powers, Kris and Ecott, Stacey and Hirshfield, Leanne M.",Through the Looking Glass: Teaching CS0 with Alice,2007,FLP: other: block languages,http://doi.acm.org/10.1145/1227310.1227386,31
# "Layman, Lucas and Williams, Laurie and Slaten, Kelli",Note to Self: Make Assignments Meaningful,2007,LA: assessment: authentic assessment,http://doi.acm.org/10.1145/1227310.1227466,31
# "Ma, Linxiao and Ferguson, John and Roper, Marc and Wood, Murray",Investigating the Viability of Mental Models Held by Novice Programmers,2007,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/1227310.1227481,26
# "Townsend, Gloria Childress and Menzel, Suzanne and Siek, Katie A.",Leveling the CS1 Playing Field,2007,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/1227310.1227428,6
# "Chen, Tzu-Yi and Lewandowski, Gary and McCartney, Robert and Sanders, Kate and Simon, Beth",Commonsense Computing: Using Student Sorting Abilities to Improve Instruction,2007,Students: predicting and measuring success,http://doi.acm.org/10.1145/1227310.1227408,8
# "Wick, Michael R.",Bridging the Conceptual Gap: Assessing the Impact on Student Attitudes Toward Programming,2007,Students: prior knowledge: concept inventories; geek genes; misconceptions,http://doi.acm.org/10.1145/1227310.1227483,7
# "Wortman, Dana and Rheingans, Penny",Visualizing Trends in Student Performance Across Computer Science Courses,2007,Students: retention,http://doi.acm.org/10.1145/1227310.1227458,4
# "Boyer, Kristy Elizabeth and Dwight, Rachael S. and Miller, Carolyn S. and Raubenheimer, C. Dianne and Stallmann, Matthias F. and Vouk, Mladen A.",A Case for Smaller Class Size with Integrated Lab for Introductory Computer Science,2007,Students: retention,http://doi.acm.org/10.1145/1227310.1227430,10
# "Turner, Elise H. and Albert, Erik and Turner, Roy M. and Latour, Laurence",Retaining Majors Through the Introductory Sequence,2007,Students: retention,http://doi.acm.org/10.1145/1227310.1227321,10
# "Leutenegger, Scott and Edgington, Jeffrey",A Games First Approach to Teaching Introductory Programming,2007,Teaching: games,http://doi.acm.org/10.1145/1227310.1227352,71
# "Murtagh, Thomas P.",Squint: Barely Visible Library Support for CS1,2007,Tools: libraries etc,http://doi.acm.org/10.1145/1227310.1227489,1
# "Robbins, Steven",A Java Execution Simulator,2007,Tools: other,http://doi.acm.org/10.1145/1227310.1227491,2
# "Beck, Leland L. and Chizhik, Alexander W.",An Experimental Study of Cooperative Learning in Cs1,2008,CA: other,http://doi.acm.org/10.1145/1352135.1352208,12
# "Braught, Grant and Eby, L. Martin and Wahls, Tim",The Effects of Pair-programming on Individual Programming Skill,2008,CA: pair programming,http://doi.acm.org/10.1145/1352135.1352207,29
# "Dodds, Zachary and Libeskind-Hadas, Ran and Alvarado, Christine and Kuenning, Geoff",Evaluating a Breadth-first Cs 1 for Scientists,2008,Content: other: breadth-first or depth-first CS1,http://doi.acm.org/10.1145/1352135.1352229,20
# "Sloan, Robert H. and Troy, Patrick",CS 0.5: A Better Approach to Introductory Computer Science for Majors,2008,Content: other: media computation,http://doi.acm.org/10.1145/1352135.1352230,15
# "Rao, T. M. and Mitra, Sandeep","An Early Software Engineering Approach to Teaching Cs1, Cs2 and Ai",2008,Content: software engineering approaches,http://doi.acm.org/10.1145/1352135.1352185,1
# "Taylor, Blair and Azadegan, Shiva",Moving Beyond Security Tracks: Integrating Security in Cs0 and Cs1,2008,Content: upper level topics in CS1,http://doi.acm.org/10.1145/1352135.1352246,16
# "Jin, Wei",Pre-programming Analysis Tutors Help Students Learn Basic Programming Concepts,2008,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/1352135.1352231,5
# "Starr, Christopher W. and Manaris, Bill and Stalvey, RoxAnn H.",Bloom's Taxonomy Revisited: Specifying Assessable Learning Objectives in Computer Science,2008,DSA: other,http://doi.acm.org/10.1145/1352135.1352227,24
# "Gries, David",A Principled Approach to Teaching OO First,2008,FLP: specific paradigms,http://doi.acm.org/10.1145/1352135.1352149,19
# "Sanders, Kate and Boustedt, Jonas and Eckerdal, Anna and McCartney, Robert and Mostr\""{o}m, Jan Erik and Thomas, Lynda and Zander, Carol",Student Understanding of Object-oriented Programming As Expressed in Concept Maps,2008,FLP: specific paradigms,http://doi.acm.org/10.1145/1352135.1352251,20
# "Sudol, Leigh Ann",Forging Connections Between Life and Class Using Reading Assignments: A Case Study,2008,LA: assessment: authentic assessment,http://doi.acm.org/10.1145/1352135.1352257,3
# "Reges, Stuart","The Mystery of ""B := (B = False)""",2008,LA: assessment: exams,http://doi.acm.org/10.1145/1352135.1352147,13
# "Cliburn, Daniel C. and Miller, Susan","Games, Stories, or Something More Traditional: The Types of Assignments College Students Prefer",2008,LA: assessment: general,http://doi.acm.org/10.1145/1352135.1352184,17
# "Fu, Xiang and Peltsverger, Boris and Qian, Kai and Tao, Lixin and Liu, Jigang",APOGEE: Automated Project Grading and Instant Feedback System for Web Based Computing,2008,LA: assessment: other: automatic feedback and/or grading,http://doi.acm.org/10.1145/1352135.1352163,9
# "Ma, Linxiao and Ferguson, John D. and Roper, Marc and Ross, Isla and Wood, Murray",Using Cognitive Conflict and Visualisation to Improve Mental Models Held by Novice Programmers,2008,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/1352135.1352253,9
# "Nienaltowski, Marie-H{\'e}l\`{e}ne and Pedroni, Michela and Meyer, Bertrand",Compiler Error Messages: What Can Help Novices?,2008,LA: learning: errors,http://doi.acm.org/10.1145/1352135.1352192,21
# "Murphy, Christian and Kim, Eunhee and Kaiser, Gail and Cannon, Adam",Backstop: A Tool for Debugging Runtime Errors,2008,LA: learning: errors,http://doi.acm.org/10.1145/1352135.1352193,7
# "Pearce, Janice and Nakazawa, Mario",The Funnel That Grew Our Cis Major in the Cs Desert,2008,Students: retention,http://doi.acm.org/10.1145/1352135.1352304,15
# "Repenning, Alexander and Ioannidou, Andri",Broadening Participation Through Scalable Game Design,2008,Teaching: games,http://doi.acm.org/10.1145/1352135.1352242,15
# "Head, Christopher C. D. and Wolfman, Steven A.","Poogle and the Unknown-answer Assignment: Open-ended, Sharable Cs1 Assignments",2008,Teaching: model problems and examples,http://doi.acm.org/10.1145/1352135.1352183,3
# "Sung, Kelvin and Panitz, Michael and Wallace, Scott and Anderson, Ruth and Nordlinger, John",Game-themed Programming Assignments: The Faculty Perspective,2008,Teaching: model problems and examples,http://doi.acm.org/10.1145/1352135.1352241,19
# "Murphy, Laurie and Lewandowski, Gary and McCauley, Ren{\'e}e and Simon, Beth and Thomas, Lynda and Zander, Carol","Debugging: The Good, the Bad, and the Quirky -- a Qualitative Analysis of Novices' Strategies",2008,Tools: debugging and testing,http://doi.acm.org/10.1145/1352135.1352191,20
# "Janzen, David and Saiedian, Hossein",Test-driven Learning in Early Programming Courses,2008,Tools: debugging and testing,http://doi.acm.org/10.1145/1352135.1352315,23
# "Thornton, Matthew and Edwards, Stephen H. and Tan, Roy P. and P{\'e}rez-Qui\~{n}ones, Manuel A.",Supporting Student-written Tests of Gui Programs,2008,Tools: debugging and testing,http://doi.acm.org/10.1145/1352135.1352316,8
# "Corliss, Marc L. and Lewis, E. Christopher","Bantam: A Customizable, Java-based, Classroom Compiler",2008,Tools: editors apis etc,http://doi.acm.org/10.1145/1352135.1352153,7
# "Frost, Daniel","Ucigame, a Java Library for Games",2008,Tools: libraries etc,http://doi.acm.org/10.1145/1352135.1352243,2
# "Hanks, Brian and Brandt, Matt",Successful and Unsuccessful Problem Solving Approaches of Novice Programmers,2009,CA: pair programming,http://doi.acm.org/10.1145/1508865.1508876,3
# "Hanks, Brian and Murphy, Laurie and Simon, Beth and McCauley, Ren{\'e}e and Zander, Carol",CS1 Students Speak: Advice for Students by Students,2009,CA: peer instruction,http://doi.acm.org/10.1145/1508865.1508875,12
# "Hundhausen, Christopher and Agrawal, Anukrati and Fairbrother, Dana and Trevisan, Michael",Integrating Pedagogical Code Reviews into a CS 1 Course: An Empirical Study,2009,Content: software engineering approaches,http://doi.acm.org/10.1145/1508865.1508972,21
# "Stepp, Marty and Miller, Jessica and Kirst, Victoria","A ""CS 1.5"" Introduction to Web Programming",2009,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/1508865.1508908,12
# "Gal-Ezer, Judith and Vilner, Tamar and Zur, Ela",Has the Paradigm Shift in CS1 a Harmful Effect on Data Structures Courses: A Case Study,2009,FLP: specific paradigms,http://doi.acm.org/10.1145/1508865.1508909,6
# "Enbody, Richard J. and Punch, William F. and McCullen, Mark",Python CS1 As Preparation for C++ CS2,2009,FLP: specific text-based languages,http://doi.acm.org/10.1145/1508865.1508907,14
# "Gehringer, Edward F. and Miller, Carolyn S.",Student-generated Active-learning Exercises,2009,LA: assessment: other: auto and student generated assignments,http://doi.acm.org/10.1145/1508865.1508897,10
# "Cicirello, Vincent A.",On the Role and Effectiveness of Pop Quizzes in CS1,2009,LA: assessment: other: homework and quizzes,http://doi.acm.org/10.1145/1508865.1508971,3
# "Philpott, Anne and Clear, Tony and Whalley, Jacqueline",Understanding Student Performance on an Algorithm Simulation Task: Implications for Guided Learning,2009,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/1508865.1509012,1
# "Desai, Chetan and Janzen, David S. and Clements, John",Implications of Integrating Test-driven Development into CS1/CS2 Curricula,2009,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/1508865.1508921,22
# "Cavender, Anna C. and Ladner, Richard E. and Roth, Robert I.",The Summer Academy for Advancing Deaf and Hard of Hearing in Computing,2009,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/1508865.1509043,4
# "Fenwick,Jr., James B. and Norris, Cindy and Barry, Frank E. and Rountree, Josh and Spicer, Cole J. and Cheek, Scott D.",Another Look at the Behaviors of Novice Programmers,2009,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/1508865.1508973,15
# "Murphy, Christian and Kaiser, Gail and Loveland, Kristin and Hasan, Sahar",Retina: Helping Students and Instructors Based on Observed Programming Activities,2009,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/1508865.1508929,24
# "Barker, Lecia J. and McDowell, Charlie and Kalahar, Kimberly",Exploring Factors That Influence Computer Science Introductory Course Students to Persist in the Major,2009,Students: retention,http://doi.acm.org/10.1145/1508865.1508923,46
# "Bayliss, Jessica D.",Using Games in Introductory Courses: Tips from the Trenches,2009,Teaching: games,http://doi.acm.org/10.1145/1508865.1508989,14
# "Luxton-Reilly, Andrew and Denny, Paul",A Simple Framework for Interactive Games in CS1,2009,Teaching: games,http://doi.acm.org/10.1145/1508865.1508947,10
# "Eagle, Michael and Barnes, Tiffany",Experimental Evaluation of an Educational Game for Improved Learning in Introductory Computing,2009,Teaching: games,http://doi.acm.org/10.1145/1508865.1508980,29
# "Summet, Jay and Kumar, Deepak and O'Hara, Keith and Walker, Daniel and Ni, Lijun and Blank, Doug and Balch, Tucker",Personalizing CS1 with Robots,2009,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/1508865.1509018,43
# "Lauwers, Tom and Nourbakhsh, Illah and Hamner, Emily",CSbots: Design and Deployment of a Robot Designed for the CS1 Classroom,2009,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/1508865.1509017,15
# "McWhorter, William Isaac and O'Connor, Brian C.",Do LEGO\textregistered Mindstorms\textregistered Motivate Students in CS1?,2009,Teaching: hardware (robots etc),http://doi.acm.org/10.1145/1508865.1509019,18
# "Flatland, Robin Y. and Matthews, James R.",Using Modes of Inquiry and Engaging Problems to Link Computer Science and Mathematics,2009,Teaching: model problems and examples,http://doi.acm.org/10.1145/1508865.1509002,0
# "Bennett, Chris and Urness, Timothy",Using Daily Student Presentations to Address Attitudes and Communication Skills in CS1,2009,Teaching: other,http://doi.acm.org/10.1145/1508865.1508896,3
# "Goldwasser, Michael H. and Letscher, David",A Graphics Package for the First Day and Beyond,2009,Tools: libraries etc,http://doi.acm.org/10.1145/1508865.1508945,2
# "Boland, Michael G. and Clifton, Curtis",Introducing PyLighter: Dynamic Code Highlighter,2009,Tools: other,http://doi.acm.org/10.1145/1508865.1509037,0
# "Hundhausen, Christopher and Agrawal, Anukrati and Fairbrother, Dana and Trevisan, Michael",Does Studio-based Instruction Work in CS 1?: An Empirical Comparison with a Traditional Approach,2010,CA: other,http://doi.acm.org/10.1145/1734263.1734432,16
# "Braught, Grant and MacCormick, John and Wahls, Tim",The Benefits of Pairing by Ability,2010,CA: pair programming,http://doi.acm.org/10.1145/1734263.1734348,12
# "Simon, Beth and Kohanfars, Michael and Lee, Jeff and Tamayo, Karen and Cutts, Quintin",Experience Report: Peer Instruction in Introductory Computing,2010,CA: peer instruction,http://doi.acm.org/10.1145/1734263.1734381,43
# "Hundhausen, Christopher and Agrawal, Anukrati and Ryan, Kyle",The Design of an Online Environment to Support Pedagogical Code Reviews,2010,Content: software engineering approaches,http://doi.acm.org/10.1145/1734263.1734324,8
# "Bruce, Kim B. and Danyluk, Andrea and Murtagh, Thomas",Introducing Concurrency in CS 1,2010,Content: upper level topics in CS1,http://doi.acm.org/10.1145/1734263.1734341,13
# "Hertz, Matthew","What Do ""CS1"" and ""CS2"" Mean?: Investigating Differences in the Early Courses",2010,DSA: general,http://doi.acm.org/10.1145/1734263.1734335,14
# "Malan, David J.",Reinventing CS50,2010,DSA: general,http://doi.acm.org/10.1145/1734263.1734316,6
# "Enbody, Richard J. and Punch, William F.",Performance of Python CS1 Students in Mid-level Non-python CS Courses,2010,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/1734263.1734437,6
# "Ambr\'{o}sio, Ana Paula L. and Costa, F\'{a}bio M.",Evaluating the Impact of PBL and Tablet PCs in an Algorithms and Computer Programming Course,2010,DSA: other,http://doi.acm.org/10.1145/1734263.1734431,1
# "Denny, Paul and Hanks, Brian and Simon, Beth",Peerwise: Replication Study of a Student-collaborative Self-testing Web Service in a U.S. Setting,2010,LA: assessment: other: auto and student generated assignments,http://doi.acm.org/10.1145/1734263.1734407,9
# "Alvarado, Christine and Dodds, Zachary",Women in CS: An Evaluation of Three Promising Practices,2010,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/1734263.1734281,28
# "Tew, Allison Elliott and Guzdial, Mark",Developing a Validated Assessment of Fundamental CS1 Concepts,2010,Students: prior knowledge: concept inventories; geek genes; misconceptions,http://doi.acm.org/10.1145/1734263.1734297,41
# "Kaczmarczyk, Lisa C. and Petrick, Elizabeth R. and East, J. Philip and Herman, Geoffrey L.",Identifying Student Misconceptions of Programming,2010,Students: prior knowledge: concept inventories; geek genes; misconceptions,http://doi.acm.org/10.1145/1734263.1734299,27
# "Cutts, Quintin and Cutts, Emily and Draper, Stephen and O'Donnell, Patrick and Saffrey, Peter",Manipulating Mindset to Positively Influence Introductory Programming Performance,2010,Students: retention,http://doi.acm.org/10.1145/1734263.1734409,14
# "Boyer, Kristy Elizabeth and Lahti, William and Phillips, Robert and Wallis, Michael D. and Vouk, Mladen A. and Lester, James C.",Principles of Asking Effective Questions During Student Problem Solving,2010,Teaching: aids examples tricks,http://doi.acm.org/10.1145/1734263.1734417,4
# "Schuster, Daniel L.","CS1, Arcade Games and the Free Java Book",2010,Teaching: games,http://doi.acm.org/10.1145/1734263.1734445,3
# "Hillyard, Cinnamon and Angotti, Robin and Panitz, Michael and Sung, Kelvin and Nordlinger, John and Goldstein, David",Game-themed Programming Assignments for Faculty: A Case Study,2010,Teaching: games,http://doi.acm.org/10.1145/1734263.1734358,6
# "Chavey, Darrah P.",Double Sorting: Testing Their Sorting Skills,2010,Teaching: model problems and examples,http://doi.acm.org/10.1145/1734263.1734392,0
# "Stepp, Michael and Simon, Beth",Introductory Computing Students' Conceptions of Illegal Student-student Collaboration,2010,Teaching: other: plagiarism,http://doi.acm.org/10.1145/1734263.1734365,6
# "Tenenbaum, Aaron and Weiss, Gerald and Arnow, David",Monetary Values: Double Trouble or Dollars and Sense?,2010,Teaching: specific topics (arrays recursion etc),http://doi.acm.org/10.1145/1734263.1734391,0
# "Carlisle, Martin C.",Using You Tube to Enhance Student Class Preparation in an Introductory Java Course,2010,Teaching: video,http://doi.acm.org/10.1145/1734263.1734419,5
# "Radermacher, Alex D. and Walia, Gursimran S.",Investigating the Effective Implementation of Pair Programming: An Empirical Investigation,2011,CA: pair programming,http://doi.acm.org/10.1145/1953163.1953346,4
# "Murphy, Christian and Powell, Rita and Parton, Kristen and Cannon, Adam",Lessons Learned from a PLTL-CS Program,2011,CA: peer instruction,http://doi.acm.org/10.1145/1953163.1953226,3
# "VanDeGrift, Tammy and Caruso, Tamara and Hill, Natalie and Simon, Beth",Experience Report: Getting Novice Programmers to THINK About Improving Their Software Development Process,2011,Content: software engineering approaches,http://doi.acm.org/10.1145/1953163.1953307,7
# "Garrity, Patrick and Yates, Timothy and Brown, Richard and Shoop, Elizabeth",WebMapReduce: An Accessible and Adaptable Tool for Teaching Map-reduce Computing,2011,Content: upper level topics in CS1,http://doi.acm.org/10.1145/1953163.1953221,16
# "Hundhausen, Christopher D. and Agarwal, Pawan and Trevisan, Michael",Online vs. Face-to-face Pedagogical Code Reviews: An Empirical Comparison,2011,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/1953163.1953201,3
# "Jin, Wei and Corbett, Albert",Effectiveness of Cognitive Apprenticeship Learning (CAL) and Cognitive Tutors (CT) for Problem Solving Using Fundamental Programming Concepts,2011,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/1953163.1953254,3
# "Denny, Paul and Luxton-Reilly, Andrew and Tempero, Ewan and Hendrickx, Jacob",CodeWrite: Supporting Student-driven Practice of Java,2011,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/1953163.1953299,22
# "Petersen, Andrew and Craig, Michelle and Zingaro, Daniel",Reviewing CS1 Exam Question Content,2011,LA: assessment: exams,http://doi.acm.org/10.1145/1953163.1953340,32
# "Marceau, Guillaume and Fisler, Kathi and Krishnamurthi, Shriram",Measuring the Effectiveness of Error Messages Designed for Novice Programmers,2011,LA: learning: errors,http://doi.acm.org/10.1145/1953163.1953308,16
# "Cohoon, James P. and Tychonievich, Luther A.",Analysis of a CS1 Approach for Attracting Diverse and Inexperienced Students to Computing Majors,2011,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/1953163.1953217,8
# "Dyke, Gregory",Which Aspects of Novice Programmers' Usage of an IDE Predict Learning Outcomes,2011,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/1953163.1953309,9
# "Tew, Allison Elliott and Guzdial, Mark",The FCS1: A Language Independent Assessment of CS1 Knowledge,2011,Students: prior knowledge: concept inventories; geek genes; misconceptions,http://doi.acm.org/10.1145/1953163.1953200,33
# "Shinners-Kennedy, Dermot and Barnes, David J.","The Novice Programmer's ""Device to Think with""",2011,Teaching: aids examples tricks,http://doi.acm.org/10.1145/1953163.1953310,0
# "Drake, Peter and Sung, Kelvin",Teaching Introductory Programming with Popular Board Games,2011,Teaching: games,http://doi.acm.org/10.1145/1953163.1953338,9
# "Davies, Stephen and Polack-Wahl, Jennifer A. and Anewalt, Karen",A Snapshot of Current Practices in Teaching the Introductory Programming Sequence,2011,Teaching: general,http://doi.acm.org/10.1145/1953163.1953339,13
# "Hubwieser, Peter and Berges, Marc",Minimally Invasive Programming Courses: Learning OOP with(out) Instruction,2011,Teaching: other,http://doi.acm.org/10.1145/1953163.1953195,5
# "Chamillard, A. T.",Using a Student Response System in CS1 and CS2,2011,Teaching: other,http://doi.acm.org/10.1145/1953163.1953253,5
# "Miller, L. D. and Soh, Leen-Kiat and Nugent, Gwen and Kupzyk, Kevin and Masmaliyeva, Leyla and Samal, Ashok",Evaluating the Use of Learning Objects in CS1,2011,Teaching: other,http://doi.acm.org/10.1145/1953163.1953183,0
# "Stone, Jeffrey A. and Clark, Tricia K.",The Impact of Problem-oriented Animated Learning Modules in a CS1-style Course,2011,Teaching: video,http://doi.acm.org/10.1145/1953163.1953182,2
# "Jenkins, Jam and Brannock, Evelyn and Cooper, Thomas and Dekhane, Sonal and Hall, Mark and Nguyen, Michael",Perspectives on Active Learning and Collaboration: JavaWIDE in the Classroom,2012,CA: other: collaborative tools,http://doi.acm.org/10.1145/2157136.2157194,4
# "Scaffidi, Christopher and Dahotre, Aniket and Zhang, Yan",How Well Do Online Forums Facilitate Discussion and Collaboration Among Novice Animation Programmers?,2012,CA: other: collaborative tools,http://doi.acm.org/10.1145/2157136.2157195,3
# "Radermacher, Alex and Walia, Gursimran and Rummelt, Richard",Assigning Student Programming Pairs Based on Their Mental Model Consistency: An Initial Investigation,2012,CA: pair programming,http://doi.acm.org/10.1145/2157136.2157236,4
# "Sprenkle, Sara and Duvall, Shannon",Reshaping the Image of Computer Science in Only Fifteen Minutes (of Class) a Week,2012,Content: other,http://doi.acm.org/10.1145/2157136.2157308,1
# "Haungs, Michael and Clark, Christopher and Clements, John and Janzen, David",Improving First-year Success and Retention Through Interest-based CS0 Courses,2012,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/2157136.2157307,18
# "Zingaro, Daniel and Petersen, Andrew and Craig, Michelle",Stepping Up to Integrative Questions on CS1 Exams,2012,LA: assessment: exams,http://doi.acm.org/10.1145/2157136.2157215,6
# "Gluga, Richard and Kay, Judy and Lister, Raymond and Kleitman, Sabina and Lever, Tim",Over-confidence and Confusion in Using Bloom for Programming Fundamentals Assessment,2012,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/2157136.2157181,9
# "Craig, Michelle and Petersen, Sarah and Petersen, Andrew",Following a Thread: Knitting Patterns and Program Tracing,2012,LA: learning: other,http://doi.acm.org/10.1145/2157136.2157204,4
# "Murphy, Laurie and McCauley, Ren{\'e}e and Fitzgerald, Sue",'Explain in Plain English' Questions: Implications for Teaching,2012,LA: learning: other,http://doi.acm.org/10.1145/2157136.2157249,10
# "Jamieson, Alan C. and Jamieson, Lindsay H. and Johnson, Angela C.",Application of Non-programming Focused Treisman-style Workshops in Introductory Computer Science,2012,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/2157136.2157219,0
# "Piech, Chris and Sahami, Mehran and Koller, Daphne and Cooper, Steve and Blikstein, Paulo",Modeling How Students Learn to Program,2012,Students: predicting and measuring success,http://doi.acm.org/10.1145/2157136.2157182,40
# "Carter, Paul",An Experience Report: On the Use of Multimedia Pre-instruction and Just-in-time Teaching in a CS1 Course,2012,Teaching: other,http://doi.acm.org/10.1145/2157136.2157244,10
# "Stone, Jeffrey A.",Using Reflective Blogs for Pedagogical Feedback in CS1,2012,Teaching: other,http://doi.acm.org/10.1145/2157136.2157216,3
# "Greenberg, Ira and Kumar, Deepak and Xu, Dianna",Creative Coding and Visual Portfolios for CS1,2012,Teaching: other,http://doi.acm.org/10.1145/2157136.2157214,14
# "Vilner, Tamar and Zur, Ela and Sagi, Ronit",Integrating Video Components in CS1,2012,Teaching: video,http://doi.acm.org/10.1145/2157136.2157176,3
# "Blank, Douglas and Kay, Jennifer S. and Marshall, James B. and O'Hara, Keith and Russo, Mark","Calico: A Multi-programming-language, Multi-context Framework Designed for Computer Science Education",2012,Tools: editors apis etc,http://doi.acm.org/10.1145/2157136.2157158,2
# "Dewan, Prasun",How a Language-based GUI Generator Can Influence the Teaching of Object-oriented Programming,2012,Tools: visualization,http://doi.acm.org/10.1145/2157136.2157159,0
# "Zingaro, Daniel and Bailey Lee, Cynthia and Porter, Leo",Peer Instruction in Computing: The Role of Reading Quizzes,2013,CA: peer instruction,http://doi.acm.org/10.1145/2445196.2445216,14
# "Rebelsky, Samuel A. and Davis, Janet and Weinman, Jerod",Building Knowledge and Confidence with Mediascripting: A Successful Interdisciplinary Approach to CS1,2013,Content: other: media computation,http://doi.acm.org/10.1145/2445196.2445342,3
# "Ko, Yousun and Burgstaller, Bernd and Scholz, Bernhard",Parallel from the Beginning: The Case for Multicore Programming in Thecomputer Science Undergraduate Curriculum,2013,Content: upper level topics in CS1,http://doi.acm.org/10.1145/2445196.2445320,2
# "Pournaghshband, Vahab",Teaching the Security Mindset to CS1 Students,2013,Content: upper level topics in CS1,http://doi.acm.org/10.1145/2445196.2445299,1
# "Esper, Sarah and Foster, Stephen R. and Griswold, William G.",On the Nature of Fires and How to Spark Them when You'Re Not There,2013,DSA PS: other,http://doi.acm.org/10.1145/2445196.2445290,6
# "Black, Andrew P. and Bruce, Kim B. and Homer, Michael and Noble, James and Ruskin, Amy and Yannow, Richard",Seeking Grace: A New Object-oriented Language for Novices,2013,FLP: specific paradigms,http://doi.acm.org/10.1145/2445196.2445240,9
# "Razak, Saquib",A Case for Course Capstone Projects in CS1,2013,LA: assessment: other: projects,http://doi.acm.org/10.1145/2445196.2445398,1
# "Ginat, David and Shmalo, Ronit",Constructive Use of Errors in Teaching CS1,2013,LA: learning: errors,http://doi.acm.org/10.1145/2445196.2445300,4
# "Hertz, Matthew and Ford, Sarah Michele",Investigating Factors of Student Learning in Introductory Courses,2013,LA: learning: general learning,http://doi.acm.org/10.1145/2445196.2445254,2
# "Anderson, Nicole and Gegg-Harrison, Tim","Learning Computer Science in the ""Comfort Zone of Proximal Development""",2013,LA: learning: learning styles,http://doi.acm.org/10.1145/2445196.2445344,2
# "Lee, Cynthia Bailey","Experience Report: CS1 in MATLAB for Non-majors, with Media Computation and Peer Instruction",2013,Students: non-majors,http://doi.acm.org/10.1145/2445196.2445214,7
# "Lawrance, Joseph and Jung, Seikyung and Wiseman, Charles",Git on the Cloud in the Classroom,2013,Students: non-majors,http://doi.acm.org/10.1145/2445196.2445386,5
# "Sullivan, David G.",A Data-centric Introduction to Computer Science for Non-majors,2013,Students: non-majors,http://doi.acm.org/10.1145/2445196.2445222,12
# "Tafliovich, Anya and Campbell, Jennifer and Petersen, Andrew",A Student Perspective on Prior Experience in CS1,2013,Students: prior knowledge,http://doi.acm.org/10.1145/2445196.2445270,8
# "Porter, Leo and Simon, Beth",Retaining Nearly One-third More Majors with a Trio of Instructional Best Practices in CS1,2013,Students: retention,http://doi.acm.org/10.1145/2445196.2445248,51
# "Decker, Adrienne and Lawley, Elizabeth Lane",Life's a Game and the Game of Life: How Making a Game out of It Can Change Student Behavior,2013,Students: retention,http://doi.acm.org/10.1145/2445196.2445269,7
# "Hertz, Matthew and Jump, Maria",Trace-based Teaching in Early Programming Courses,2013,Teaching: aids examples tricks,http://doi.acm.org/10.1145/2445196.2445364,7
# "Lockwood, Kate and Esselstein, Rachel",The Inverted Classroom and the CS Curriculum,2013,Teaching: flipped approaches,http://doi.acm.org/10.1145/2445196.2445236,20
# "Rubin, Marc J.",The Effectiveness of Live-coding to Teach Introductory Programming,2013,Teaching: other,http://doi.acm.org/10.1145/2445196.2445388,10
# "Bayzick, Jennifer and Askins, Bradley and Kalafut, Sharon and Spear, Michael",Reading Mobile Games Throughout the Curriculum,2013,Tools: editors apis etc,http://doi.acm.org/10.1145/2445196.2445264,5
# "Zingaro, Daniel and Cherenkova, Yuliya and Karpova, Olessia and Petersen, Andrew",Facilitating Code-writing in PI Classes,2013,Tools: other,http://doi.acm.org/10.1145/2445196.2445369,15
# "Guo, Philip J.",Online Python Tutor: Embeddable Web-based Program Visualization for Cs Education,2013,Tools: visualization,http://doi.acm.org/10.1145/2445196.2445368,51
# "Hu, Helen H. and Shepherd, Tricia D.",Teaching CS 1 with POGIL Activities and Roles,2014,CA: other,http://doi.acm.org/10.1145/2538862.2538954,12
# "Zarb, Mark and Hughes, Janet and Richards, John",Evaluating Industry-inspired Pair Programming Communication Guidelines with Undergraduate Students,2014,CA: pair programming,http://doi.acm.org/10.1145/2538862.2538980,1
# "Zingaro, Daniel",Peer Instruction Contributes to Self-efficacy in CS1,2014,CA: peer instruction,http://doi.acm.org/10.1145/2538862.2538878,17
# "Warren, Joe and Rixner, Scott and Greiner, John and Wong, Stephen",Facilitating Human Interaction in an Online Programming Course,2014,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/2538862.2538893,5
# "Bart, Austin Cory and Tilevich, Eli and Hall, Simin and Allevato, Tony and Shaffer, Clifford A.",Transforming Introductory Computer Science Projects via Real-time Web Data,2014,LA: assessment: authentic assessment,http://doi.acm.org/10.1145/2538862.2538941,6
# "Gaudencio, Matheus and Dantas, Ayla and Guerrero, Dalton D.S.",Can Computers Compare Student Code Solutions As Well As Teachers?,2014,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/2538862.2538973,3
# "Moreno, Andr{\'e}s and Sutinen, Erkki and Joy, Mike",Defining and Evaluating Conflictive Animations for Programming Education: The Case of Jeliot ConAn,2014,LA: learning: errors,http://doi.acm.org/10.1145/2538862.2538888,1
# "DeNero, John and Martinis, Stephen",Teaching Composition Quality at Scale: Human Judgment in the Age of Autograders,2014,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/2538862.2538976,2
# "Charters, Polina and Lee, Michael J. and Ko, Andrew J. and Loksa, Dastyni",Challenging Stereotypes and Changing Attitudes: The Effect of a Brief Programming Encounter on Adults' Attitudes Toward Programming,2014,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/2538862.2538938,8
# "Davis, Don and Yuen, Timothy and Berland, Matthew",Multiple Case Study of Nerd Identity in a CS1 Class,2014,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/2538862.2538960,2
# "Kane, Shaun K. and Bigham, Jeffrey P.","Tracking @Stemxcomet: Teaching Programming to Blind Students via 3D Printing, Crisis Management, and Twitter",2014,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/2538862.2538975,17
# "Collier, Robert Don and Kawash, Jalal",Lessons Learned and Recommended Strategies for Game Development Components in a Computer Literacy Course,2014,Students: non-majors,http://doi.acm.org/10.1145/2538862.2538887,0
# "Cherenkova, Yuliya and Zingaro, Daniel and Petersen, Andrew",Identifying Challenging CS1 Concepts in a Large Problem Dataset,2014,Students: predicting and measuring success,http://doi.acm.org/10.1145/2538862.2538966,10
# "Porter, Leo and Zingaro, Daniel",Importance of Early Performance in CS1: Two Conflicting Assessment Stories,2014,Students: predicting and measuring success,http://doi.acm.org/10.1145/2538862.2538912,8
# "Alvarado, Christine and Lee, Cynthia Bailey and Gillespie, Gary","New CS1 Pedagogies and Curriculum, the Same Success Factors?",2014,Students: predicting and measuring success,http://doi.acm.org/10.1145/2538862.2538897,8
# "Watson, Christopher and Li, Frederick W.B. and Godwin, Jamie L.",No Tests Required: Comparing Traditional and Dynamic Predictors of Programming Success,2014,Students: predicting and measuring success,http://doi.acm.org/10.1145/2538862.2538930,36
# "Heinonen, Kenny and Hirvikoski, Kasper and Luukkainen, Matti and Vihavainen, Arto",Using CodeBrowser to Seek Differences Between Novice Programmers,2014,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/2538862.2538981,4
# "Brown, Neil Christopher Charles and K\""{o}lling, Michael and McCall, Davin and Utting, Ian",Blackbox: A Large Scale Repository of Novice Programmers' Activity,2014,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/2538862.2538924,18
# "Campbell, Jennifer and Horton, Diane and Craig, Michelle and Gries, Paul",Evaluating an Inverted CS1,2014,Teaching: flipped approaches,http://doi.acm.org/10.1145/2538862.2538943,14
# "Sanford, Joseph P. and Tietz, Aaron and Farooq, Saad and Guyer, Samuel and Shapiro, R. Benjamin",Metaphors We Teach by,2014,Teaching: other,http://doi.acm.org/10.1145/2538862.2538945,4
# "Miller, L. D. and Soh, Leen-Kiat and Chiriacescu, Vlad and Ingraham, Elizabeth and Shell, Duane F. and Hazley, Melissa Patterson",Integrating Computational and Creative Thinking to Improve Learning and Performance in CS1,2014,Teaching: other: computational thinking,http://doi.acm.org/10.1145/2538862.2538940,8
# "Newhall, Tia and Meeden, Lisa and Danner, Andrew and Soni, Ameet and Ruiz, Frances and Wicentowski, Richard",A Support Program for Introductory CS Courses That Improves Student Performance and Retains Students from Underrepresented Groups,2014,Teaching: other: teaching assistants and mentors,http://doi.acm.org/10.1145/2538862.2538923,11
# "Tang, Terry and Rixner, Scott and Warren, Joe",An Environment for Learning Interactive Programming,2014,Tools: editors apis etc,http://doi.acm.org/10.1145/2538862.2538908,4
# "Edwards, Stephen H. and Tilden, Daniel S. and Allevato, Anthony",Pythy: Improving the Introductory Python Programming Experience,2014,Tools: editors apis etc,http://doi.acm.org/10.1145/2538862.2538977,2
# "Ilinkin, Ivaylo",Opportunities for Android Projects in a CS1 Course,2014,Tools: other,http://doi.acm.org/10.1145/2538862.2538983,3
# "Cross, James and Hendrix, Dean and Barowski, Larry and Umphress, David",Dynamic Program Visualizations: An Experience Report,2014,Tools: visualization,http://doi.acm.org/10.1145/2538862.2538958,3
# "Zarb, Mark and Hughes, Janet and Richards, John",Further Evaluations of Industry-Inspired Pair Programming Communication Guidelines with Undergraduate Students,2015,CA: pair programming,http://doi.acm.org/10.1145/2676723.2677241,1
# "Anderson, Ruth E. and Ernst, Michael D. and Ord\'{o}\~{n}ez, Robert and Pham, Paul and Tribelhorn, Ben",A Data Programming CS1 Course,2015,Content: other: data science approach,http://doi.acm.org/10.1145/2676723.2677309,10
# "Hall-Holt, Olaf A. and Sanft, Kevin R.",Statistics-infused Introduction to Computer Science,2015,Content: other: data science approach,http://doi.acm.org/10.1145/2676723.2677218,3
# "Matsuzawa, Yoshiaki and Ohata, Takashi and Sugiura, Manabu and Sakai, Sanshiro",Language Migration in non-CS Introductory Programming Through Mutual Language Translation Environment,2015,FLP: other: language agnostic approaches,http://doi.acm.org/10.1145/2676723.2677230,6
# "Wilcox, Chris",The Role of Automation in Undergraduate Computer Science Education,2015,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/2676723.2677226,4
# "Pettit, Raymond and Homer, John and Gee, Roger and Mengel, Susan and Starbuck, Adam",An Empirical Study of Iterative Improvement in Programming Assignments,2015,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/2676723.2677279,4
# "Denny, Paul",Generating Practice Questions As a Preparation Strategy for Introductory Programming Exams,2015,LA: assessment: exams,http://doi.acm.org/10.1145/2676723.2677253,3
# "VanDeGrift, Tammy",Supporting Creativity and User Interaction in CS 1 Homework Assignments,2015,LA: assessment: other: homework and quizzes,http://doi.acm.org/10.1145/2676723.2677250,3
# "Wood, Zo\""{e} and Keen, Aaron",Building Worlds: Bridging Imperative-First and Object-Oriented Programming in CS1-CS2,2015,LA: assessment: other: projects,http://doi.acm.org/10.1145/2676723.2677249,0
# "Pokorny, Kian L.",Creating a Computer Simulator As a CS1 Student Project,2015,LA: assessment: other: projects,http://doi.acm.org/10.1145/2676723.2677210,1
# "Wittman, Barry and Pretz, Jean","Bats, Balls, and Lures: Cognitive Style in CS Education",2015,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/2676723.2677291,0
# "Keen, Aaron and Mammen, Kurt",Program Decomposition and Complexity in CS1,2015,LA: learning: learning styles,http://doi.acm.org/10.1145/2676723.2677219,2
# "Vihavainen, Arto and Miller, Craig S. and Settle, Amber",Benefits of Self-explanation in Introductory Programming,2015,LA: learning: other,http://doi.acm.org/10.1145/2676723.2677260,1
# "Sudol-DeLyser, Leigh Ann",Expression of Abstraction: Self Explanation in Code Production,2015,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/2676723.2677222,0
# "Ginat, David and Menashe, Eti",SOLO Taxonomy for Assessing Novices' Algorithmic Design,2015,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/2676723.2677311,3
# "Norman, Victor T. and Adams, Joel C.",Improving Non-CS Major Performance in CS1,2015,Students: non-majors,http://doi.acm.org/10.1145/2676723.2677214,1
# "Baldwin, Douglas","Can We ""Flip"" Non-Major Programming Courses Yet?",2015,Students: non-majors,http://doi.acm.org/10.1145/2676723.2677271,3
# "Settle, Amber and Lalor, John and Steinbach, Theresa",Reconsidering the Impact of CS1 on Novice Attitudes,2015,Students: other: (attitudes self-efficacy at-risk),http://doi.acm.org/10.1145/2676723.2677235,5
# "Carter, Jason and Dewan, Prasun and Pichiliani, Mauro",Towards Incremental Separation of Surmountable and Insurmountable Programming Difficulties,2015,Students: predicting and measuring success,http://doi.acm.org/10.1145/2676723.2677294,9
# "Altadmri, Amjad and Brown, Neil C.C.",37 Million Compilations: Investigating Novice Programming Mistakes in Large-Scale Student Data,2015,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/2676723.2677258,29
# "Spacco, Jaime and Denny, Paul and Richards, Brad and Babcock, David and Hovemeyer, David and Moscola, James and Duvall, Robert",Analyzing Student Work Patterns Using Programming Exercise Data,2015,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/2676723.2677297,13
# "Horton, Diane and Craig, Michelle","Drop, Fail, Pass, Continue: Persistence in CS1 and Beyond in Traditional and Inverted Delivery",2015,Students: retention,http://doi.acm.org/10.1145/2676723.2677273,12
# "Latulipe, Celine and Long, N. Bruce and Seminario, Carlos E.",Structuring Flipped Classes with Lightweight Teams and Gamification,2015,Teaching: flipped approaches,http://doi.acm.org/10.1145/2676723.2677240,12
# "Lacher, Lisa L. and Lewis, Mark C.",The Effectiveness of Video Quizzes in a Flipped Class,2015,Teaching: flipped approaches,http://doi.acm.org/10.1145/2676723.2677302,5
# "Blaheta, Don",Unci: A C++-based Unit-testing Framework for Intro Students,2015,Tools: debugging and testing,http://doi.acm.org/10.1145/2676723.2677228,0
# "Gaspar, Alessio and Torsella, Joni and Honken, Nora and Sohoni, Sohum and Arnold, Colin",Differences in the Learning Principles Dominating Student-Student vs. Student-Instructor Interactions While Working on Programming Tasks,2016,CA: other,http://doi.acm.org/10.1145/2839509.2844627,1
# "Eck, Adam and Soh, Leen-Kiat and Shell, Duane F.",Investigating Differences in Wiki-based Collaborative Activities Between Student Engagement Profiles in CS1,2016,CA: other: collaborative tools,http://doi.acm.org/10.1145/2839509.2844615,0
# "McChesney, Ian",Three Years of Student Pair Programming: Action Research Insights and Outcomes,2016,CA: pair programming,http://doi.acm.org/10.1145/2839509.2844565,3
# "Porter, Leo and Bouvier, Dennis and Cutts, Quintin and Grissom, Scott and Lee, Cynthia and McCartney, Robert and Zingaro, Daniel and Simon, Beth",A Multi-institutional Study of Peer Instruction in Introductory Computing,2016,CA: peer instruction,http://doi.acm.org/10.1145/2839509.2844642,7
# "Horton, Diane and Campbell, Jennifer and Craig, Michelle","Online CS1: Who Enrols, Why, and How Do They Do?",2016,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/2839509.2844578,2
# "Marling, Cindy and Juedes, David",CS0 for Computer Science Majors at Ohio University,2016,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/2839509.2844624,3
# "Wiegand, R. Paul and Bucci, Anthony and Kumar, Amruth N. and Albert, Jennifer L. and Gaspar, Alessio",A Data-Driven Analysis of Informatively Hard Concepts in Introductory Programming,2016,LA: learning: conceptual or cognitive issues (load - mental models - notional machines),http://doi.acm.org/10.1145/2839509.2844629,1
# "Becker, Brett A.",An Effective Approach to Enhancing Compiler Error Messages,2016,LA: learning: errors,http://doi.acm.org/10.1145/2839509.2844584,11
# "Ahadi, Alireza and Behbood, Vahid and Vihavainen, Arto and Prior, Julia and Lister, Raymond",Students' Syntactic Mistakes in Writing Seven Different Types of SQL Queries and Its Application to Predicting Students' Success,2016,LA: learning: errors,http://doi.acm.org/10.1145/2839509.2844640,7
# "Castro, Francisco Enrique Vicente and Fisler, Kathi",On the Interplay Between Bottom-Up and Datatype-Driven Program Design,2016,LA: learning: learning styles,http://doi.acm.org/10.1145/2839509.2844574,3
# "Pachulski Camara, Bruno Henrique and Graciotto Silva, Marco Aur{\'e}lio",A Strategy to Combine Test-Driven Development and Test Criteria to Improve Learning of Programming Skills,2016,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/2839509.2844633,2
# "Sahami, Mehran and Piech, Chris","As CS Enrollments Grow, Are We Attracting Weaker Students?",2016,Students: other: enrollment issues,http://doi.acm.org/10.1145/2839509.2844621,4
# "Leinonen, Juho and Longi, Krista and Klami, Arto and Vihavainen, Arto",Automatic Inference of Programming Performance and Experience from Typing Patterns,2016,Students: predicting and measuring success,http://doi.acm.org/10.1145/2839509.2844612,8
# "Lishinski, Alex and Yadav, Aman and Enbody, Richard and Good, Jon",The Influence of Problem Solving Abilities on Students' Performance on Different Assessment Tasks in CS1,2016,Students: predicting and measuring success,http://doi.acm.org/10.1145/2839509.2844596,1
# "Caceffo, Ricardo and Wolfman, Steve and Booth, Kellogg S. and Azevedo, Rodolfo",Developing a Computer Science Concept Inventory for Introductory Programming,2016,Students: prior knowledge: concept inventories; geek genes; misconceptions,http://doi.acm.org/10.1145/2839509.2844559,7
# "Shell, Duane F. and Soh, Leen-Kiat and Flanigan, Abraham E. and Peteranetz, Markeya S.",Students' Initial Course Motivation and Their Achievement and Retention in College CS1 Courses,2016,Students: retention,http://doi.acm.org/10.1145/2839509.2844606,6
# "Maxwell, Bruce A. and Taylor, Stephanie R.",Comparing Outcomes Across Different Contexts in CS1,2017,Content: other: CS+X,http://doi.acm.org/10.1145/3017680.3017757,1
# "Fitzpatrick, J. Michael and L{\'e}deczi, \'{A}kos and Narasimham, Gayathri and Lafferty, Lee and Labrie, R{\'e}al and Mielke, Paul T. and Kumar, Aatish and Brady, Katherine A.",Lessons Learned in the Design and Delivery of an Introductory Programming MOOC,2017,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/3017680.3017730,1
# "Price, Thomas W. and Dong, Yihuan and Lipovac, Dragan",iSnap: Towards Intelligent Tutoring in Novice Programming Environments,2017,LA: assessment: automatic tutoring and assessment systems,http://doi.acm.org/10.1145/3017680.3017762,4
# "Cheng, Nick and Harrington, Brian",The Code Mangler: Evaluating Coding Ability Without Writing Any Code,2017,LA: assessment: exams,http://doi.acm.org/10.1145/3017680.3017704,4
# "Cao, Yingjun and Porter, Leo",Evaluating Student Learning from Collaborative Group Tests in Introductory Computing,2017,LA: assessment: exams,http://doi.acm.org/10.1145/3017680.3017729,6
# "Lovellette, Ellie and Matta, John and Bouvier, Dennis and Frye, Roger",Just the Numbers: An Investigation of Contextualization of Problems for Novice Programmers,2017,LA: assessment: general,http://doi.acm.org/10.1145/3017680.3017726,1
# "Pettit, Raymond S. and Homer, John and Gee, Roger",Do Enhanced Compiler Error Messages Help Students?: Results Inconclusive.,2017,LA: learning: errors,http://doi.acm.org/10.1145/3017680.3017768,3
# "Alqadi, Basma S. and Maletic, Jonathan I.",An Empirical Study of Debugging Patterns Among Novices Programmers,2017,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/3017680.3017761,2
# "Babes-Vroman, Monica and Juniewicz, Isabel and Lucarelli, Bruno and Fox, Nicole and Nguyen, Thu and Tjang, Andrew and Haldeman, Georgiana and Mehta, Ashni and Chokshi, Risham",Exploring Gender Diversity in CS at a Large Public R1 Research University,2017,Students: gender diversity inclusion accessibililty,http://doi.acm.org/10.1145/3017680.3017773,3
# "Sax, Linda J. and Lehman, Kathleen J. and Zavala, Christina",Examining the Enrollment Growth: Non-CS Majors in CS1 Courses,2017,Students: non-majors,http://doi.acm.org/10.1145/3017680.3017781,1
# "Castro-Wunsch, Karo and Ahadi, Alireza and Petersen, Andrew",Evaluating Neural Networks As a Method for Identifying Students in Need of Assistance,2017,Students: other: (attitudes self-efficacy at-risk),http://doi.acm.org/10.1145/3017680.3017792,1
# "Khosravi, Hassan and Cooper, Kendra M.L.",Using Learning Analytics to Investigate Patterns of Performance and Engagement in Large Classes,2017,Students: predicting and measuring success,http://doi.acm.org/10.1145/3017680.3017711,3
# "Estey, Anthony and Keuning, Hieke and Coady, Yvonne",Automatically Classifying Students in Need of Support by Detecting Changes in Programming Behaviour,2017,Students: predicting and measuring success: programming process data,http://doi.acm.org/10.1145/3017680.3017790,4
# "Kirkpatrick, Michael S. and Mayfield, Chris",Evaluating an Alternative CS1 for Students with Prior Programming Experience,2017,Students: prior knowledge,http://doi.acm.org/10.1145/3017680.3017759,5
# "Kohn, Tobias",Variable Evaluation: An Exploration of Novice Programmers' Understanding and Common Misconceptions,2017,Students: prior knowledge: concept inventories; geek genes; misconceptions,http://doi.acm.org/10.1145/3017680.3017724,2
# "Edgcomb, Alex and Vahid, Frank and Lysecky, Roman and Lysecky, Susan","Getting Students to Earnestly Do Reading, Studying, and Homework in an Introductory Programming Class",2017,Teaching: other,http://doi.acm.org/10.1145/3017680.3017732,1
# "Shell, Duane F. and Soh, Leen-Kiat and Flanigan, Abraham E. and Peteranetz, Markeya S. and Ingraham, Elizabeth",Improving Students' Learning and Achievement in CS Classrooms Through Computational Creativity Exercises That Integrate Computational and Creative Thinking,2017,Teaching: other: computational thinking,http://doi.acm.org/10.1145/3017680.3017718,1
# "Schreiber, Benjamin J. and Dougherty, John P.",Assessment of Introducing Algorithms with Video Lectures and Pseudocode Rhymed to a Melody,2017,Teaching: video,http://doi.acm.org/10.1145/3017680.3017789,1
# "Battestilli, Lina and Awasthi, Apeksha and Cao, Yingjun",Two-Stage Programming Projects: Individual Work Followed by Peer Collaboration,2018,CA: other,http://doi.acm.org/10.1145/3159450.3159486,0
# "Celepkolu, Mehmet and Boyer, Kristy Elizabeth",Thematic Analysis of Students' Reflections on Pair Programming in CS1,2018,CA: pair programming,http://doi.acm.org/10.1145/3159450.3159516,0
# "Aarne, Onni and Peltola, Petrus and Leinonen, Juho and Hellas, Arto",A Study of Pair Programming Enjoyment and Attendance Using Study Motivation and Strategy Metrics,2018,CA: pair programming,http://doi.acm.org/10.1145/3159450.3159493,0
# "Celepkolu, Mehmet and Boyer, Kristy Elizabeth",The Importance of Producing Shared Code Through Pair Programming,2018,CA: pair programming,http://doi.acm.org/10.1145/3159450.3159506,0
# "Crawford, Chris S. and Gardner-McCune, Christina and Gilbert, Juan E.",Brain-Computer Interface for Novice Programmers,2018,Content: other: CS+X,http://doi.acm.org/10.1145/3159450.3159603,0
# "Berger-Wolf, Tanya and Igic, Boris and Taylor, Cynthia and Sloan, Robert and Poretsky, Rachel","A Biology-themed Introductory CS Course at a Large, Diverse Public University",2018,Content: other: CS+X,http://doi.acm.org/10.1145/3159450.3159538,0
# "Dahlby Albright, Sarah and Klinge, Titus H. and Rebelsky, Samuel A.",A Functional Approach to Data Science in CS1,2018,Content: other: data science approach,http://doi.acm.org/10.1145/3159450.3159550,0
# "Ilves, Kalle and Leinonen, Juho and Hellas, Arto",Supporting Self-Regulated Learning with Visualizations in Online Learning Environments,2018,"DSA PS: online, remote or MOOC delivery, DSA PS: online remote or MOOC delivery",http://doi.acm.org/10.1145/3159450.3159509,0
# "Wood, Zo\""{e} J. and Clements, John and Peterson, Zachary and Janzen, David and Smith, Hugh and Haungs, Michael and Workman, Julie and Bellardo, John and DeBruhl, Bruce",Mixed Approaches to CS0: Exploring Topic and Pedagogy Variance After Six Years of CS0,2018,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/3159450.3159592,0
# "Xu, Dianna and Wolz, Ursula and Kumar, Deepak and Greenburg, Ira",Updating Introductory Computer Science with Creative Computation,2018,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/3159450.3159539,0
# "Harrington, Brian and Cheng, Nick",Tracing vs. Writing Code: Beyond the Learning Hierarchy,2018,DSA: How CS1 relates to CS0 or CS2,http://doi.acm.org/10.1145/3159450.3159530,0
# "Alhazmi, Sohail and Hamilton, Margaret and Thevathayan, Charles",CS for All: Catering to Diversity of Master's Students Through Assignment Choices,2018,DSA: other,http://doi.acm.org/10.1145/3159450.3159464,0
# "Simon and Mason, Raina and Crick, Tom and Davenport, James H. and Murphy, Ellen",Language Choice in Introductory Programming Courses at Australasian and UK Universities,2018,FLP: general,http://doi.acm.org/10.1145/3159450.3159547,0
# "Alzahrani, Nabeel and Vahid, Frank and Edgcomb, Alex and Nguyen, Kevin and Lysecky, Roman",Python Versus C++: An Analysis of Student Struggle on Small Coding Exercises in Introductory Programming Courses,2018,FLP: specific text-based languages,http://doi.acm.org/10.1145/3159450.3160586,0
# "Ball, Robert and DuHadway, Linda and Hilton, Spencer and Rague, Brian",GUI-Based vs. Text-Based Assignments in CS1,2018,LA: assessment: general,http://doi.acm.org/10.1145/3159450.3159463,0
# "Zavala, Laura and Mendoza, Benito",On the Use of Semantic-Based AIG to Automatically Generate Programming Exercises,2018,LA: assessment: other: auto and student generated assignments,http://doi.acm.org/10.1145/3159450.3159608,0
# "Becker, Brett A. and Goslin, Kyle and Glanville, Graham",The Effects of Enhanced Compiler Error Messages on a Syntax Error Debugging Test,2018,LA: learning: errors,http://doi.acm.org/10.1145/3159450.3159461,0
# "Becker, Brett A. and Murray, Cormac and Tao, Tianyi and Song, Changheng and McCartney, Robert and Sanders, Kate","Fix the First, Ignore the Rest: Dealing with Multiple Compiler Error Messages",2018,LA: learning: errors,http://doi.acm.org/10.1145/3159450.3159453,1
# "Zingaro, Daniel and Craig, Michelle and Porter, Leo and Becker, Brett A. and Cao, Yingjun and Conrad, Phill and Cukierman, Diana and Hellas, Arto and Loksa, Dastyni and Thota, Neena",Achievement Goals in CS1: Replication and Extension,2018,LA: learning: learning styles,http://doi.acm.org/10.1145/3159450.3159452,0
# "Xie, Benjamin and Nelson, Greg L. and Ko, Andrew J.",An Explicit Strategy to Scaffold Novice Program Tracing,2018,LA: learning: reading or writing or tracing or debugging or testing,http://doi.acm.org/10.1145/3159450.3159527,0
# "Dawson, Jessica Q. and Allen, Meghan and Campbell, Alice and Valair, Anasazi",Designing an Introductory Programming Course to Improve Non-Majors' Experiences,2018,Students: non-majors,http://doi.acm.org/10.1145/3159450.3159548,0
# "Munson, Jonathan P. and Zitovsky, Joshua P.",Models for Early Identification of Struggling Novice Programmers,2018,Students: other: (attitudes self-efficacy at-risk),http://doi.acm.org/10.1145/3159450.3159476,0
# "Latulipe, Celine and Rorrer, Audrey and Long, Bruce",Longitudinal Data on Flipped Class Effects on Performance in CS1 and Retention After CS1,2018,Students: predicting and measuring success,http://doi.acm.org/10.1145/3159450.3159518,0
# "Wilcox, Chris and Lionelle, Albert",Quantifying the Benefits of Prior Programming Experience in an Introductory Computer Science Course,2018,Students: prior knowledge,http://doi.acm.org/10.1145/3159450.3159480,0
# "Lacher, Lisa L. and Jiang, Albert and Zhang, Yu and Lewis, Mark C.",Including Coding Questions in Video Quizzes for a Flipped CS1,2018,Teaching: flipped approaches,http://doi.acm.org/10.1145/3159450.3159504,0
# "Garcia, Saturnino",Improving Classroom Preparedness Using Guided Practice,2018,Teaching: other,http://doi.acm.org/10.1145/3159450.3159571,0
# "Caceffo, Ricardo and Gama, Guilherme and Azevedo, Rodolfo",Exploring Active Learning Approaches to Computer Science Classes,2018,Teaching: other,http://doi.acm.org/10.1145/3159450.3159585,0
# "Izu, Cruz and Mirolo, Claudio and Weerasinghe, Amali",Novice Programmers' Reasoning About Reversing Conditional Statements,2018,Teaching: specific topics (arrays recursion etc),http://doi.acm.org/10.1145/3159450.3159499,0
# "Esteero, Ramy and Khan, Mohammed and Mohamed, Mohamed and Zhang, Larry Yueli and Zingaro, Daniel",Recursion or Iteration: Does It Matter What Students Choose?,2018,Teaching: specific topics (arrays recursion etc),http://doi.acm.org/10.1145/3159450.3159455,0
