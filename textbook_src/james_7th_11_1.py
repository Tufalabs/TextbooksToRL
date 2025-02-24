

text = """Infinite sequences and series were introduced briefly in A Preview of Calculus in connection with Zeno’s
paradoxes and the decimal representation of numbers. Their importance in calculus stems from Newton’s
idea of representing functions as sums of infinite series. For instance, in finding areas he often integrated
a function by first expressing it as a series and then integrating each term of the series. We will pursue his
idea in Section 11.10 in order to integrate such functions as . (Recall that we have previously been
unable to do this.) Many of the functions that arise in mathematical physics and chemistry, such as Bessel
functions, are defined as sums of series, so it is important to be familiar with the basic concepts of convergence of infinite sequences and series.
Physicists also use series in another way, as we will see in Section 11.11. In studying fields as diverse
as optics, special relativity, and electromagnetism, they analyze phenomena by replacing a function with
the first few terms in the series that represents it.

A sequence can be thought of as a list of numbers written in a definite order:
The number is called the first term, is the second term, and in general is the nth term.
We will deal exclusively with infinite sequences and so each term will have a successor .
Notice that for every positive integer there is a corresponding number and so a
sequence can be defined as a function whose domain is the set of positive integers. But we
usually write instead of the function notation for the value of the function at the
number .
NOTATION The sequence { , , , . . .} is also denoted by
Some sequences can be defined by giving a formula for the nth term. In the
following examples we give three descriptions of the sequence: one by using the preceding notation, another by using the defining formula, and a third by writing out the terms
of the sequence. Notice that doesn’t have to start at 1.
(a)
(b)
(c)
(d)
Find a formula for the general term of the sequence
assuming that the pattern of the first few terms continues.
SOLUTION We are given that
Notice that the numerators of these fractions start with 3 and increase by 1 whenever we
go to the next term. The second term has numerator 4, the third term has numerator 5; in
general, the th term will have numerator . The denominators are the powers of 5,
a1, a2, a3, a4, ..., an, . . .
a1 a2 an
an
an1
n an
an fn
n
a1 a2 a3
an  or an  n1

n
 n
n  1 
n1

an  n
n  1 
1
2 ,
2
3 ,
3
4 ,
4
5 , . . . , n
n  1 , . . .

1
n
n  1
3n  an  1
n
n  1
3n  2
3 ,
3
9 ,  4
27 , 5
81 , . . . , 1
n
n  1
3n , . . .
{sn  3 }n3

an  sn  3 , n  3 {0, 1, s2 , s3 , . . . , sn  3 , . . .}
cos
n
6 
n0

an  cos
n
6 , n  0 1, s3
2 ,
1
2 , 0, . . . , cos
n
6 , . . .
an

3
5 ,  4
25 , 5
125 ,  6
625 , 7
3125 , . . .
a1  3
5
a2   4
25
a3  5
125
a4   6
625
a5  7
3125
n n  2
EXAMPLE 1
v EXAMPLE 2
97909_11_ch11_p689-697.qk_97909_11_ch11_p689-69erved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
SECTION 11.1 SEQUENCES 691
so has denominator . The signs of the terms are alternately positive and negative,
so we need to multiply by a power of . In Example 1(b) the factor meant we
started with a negative term. Here we want to start with a positive term and so we use
or . Therefore
Here are some sequences that don’t have a simple defining equation.
(a) The sequence , where is the population of the world as of January 1 in the
year .
(b) If we let be the digit in the nth decimal place of the number , then is a welldefined sequence whose first few terms are
(c) The Fibonacci sequence is defined recursively by the conditions
Each term is the sum of the two preceding terms. The first few terms are
This sequence arose when the 13th-century Italian mathematician known as Fibonacci
solved a problem concerning the breeding of rabbits (see Exercise 83).
A sequence such as the one in Example 1(a), , can be pictured either by
plotting its terms on a number line, as in Figure 1, or by plotting its graph, as in Figure 2.
Note that, since a sequence is a function whose domain is the set of positive integers, its
graph consists of isolated points with coordinates
. . . . . .
From Figure 1 or Figure 2 it appears that the terms of the sequence are
approaching 1 as becomes large. In fact, the difference
can be made as small as we like by taking sufficiently large. We indicate this by writing
In general, the notation
means that the terms of the sequence approach as becomes large. Notice that the
following definition of the limit of a sequence is very similar to the definition of a limit of
a function at infinity given in Section 2.6.
an 5n
1 1 n
1 n1 1 n1
an  1 n1 n  2
5n
pn  pn
n
an e an 
7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5, . . .
 fn 
f1  1 f2  1 fn  fn1  fn2 n  3
1, 1, 2, 3, 5, 8, 13, 21, . . .
an  nn  1
1, a1 2, a2  3, a3  n, an
an  nn  1
n
1  n
n  1  1
n  1
n
lim
nl
n
n  1  1
lim
nl
an  L
an  L n
EXAMPLE 3
0 1 1
2
a¡ a™ a£
a¢
FIGURE 1
FIGURE 2
0 n
an
1
1
2 3 4 5 6 7
7
8 a¶=
97909_11_ch11_p689-697.qk_97909_11_ch11_p689-69erved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
692 CHAPTER 11 INFINITE SEQUENCES AND SERIES
Definition A sequence has the limit and we write
if we can make the terms as close to as we like by taking sufficiently large.
If exists, we say the sequence converges (or is convergent). Otherwise,
we say the sequence diverges (or is divergent).
Figure 3 illustrates Definition 1 by showing the graphs of two sequences that have the
limit .
A more precise version of Definition 1 is as follows.
Definition A sequence has the limit and we write
if for every there is a corresponding integer such that
if then
Definition 2 is illustrated by Figure 4, in which the terms , , , . . . are plotted on a
number line. No matter how small an interval is chosen, there exists an
such that all terms of the sequence from onward must lie in that interval.
Another illustration of Definition 2 is given in Figure 5. The points on the graph of
must lie between the horizontal lines and if . This picture
must be valid no matter how small is chosen, but usually a smaller requires a larger .
an  L
lim
nl
an  L or an l L as n l 
an L n
limnl an
L
0 n
an
L
0 n
an
L
FIGURE 3
Graphs of two
sequences with
lim an= L n  `
1
an  L
lim or an l L as n l  nl 
an  L
  0 N
n  N 	 an  L	 	 
a1 a2 a3
L  , L   N
aN1
FIGURE 4 0 L-∑ L L+∑
a¡ a£ a™ aˆ a a˜ a∞aß a¢ a¶ N+1 aN+2
an 
y  L   y  L   n  N
  N
2
FIGURE 5 2 0 n
y
1 3 4
L
y=L+∑
N
y=L-∑
Compare this definition with Definition 2.6.7.
97909_11_ch110 Cengage Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
SECTION 11.1 SEQUENCES 693
If you compare Definition 2 with Definition 2.6.7 you will see that the only difference
between and is that is required to be an integer. Thus we
have the following theorem, which is illustrated by Figure 6.
Theorem If and when is an integer, then
.
In particular, since we know that when (Theorem 2.6.5), we
have
if
If becomes large as n becomes large, we use the notation . The following precise definition is similar to Definition 2.6.9.
Definition means that for every positive number there is an
integer such that
if then
If , then the sequence is divergent but in a special way. We say that
diverges to .
The Limit Laws given in Section 2.3 also hold for the limits of sequences and their proofs
are similar.
If and are convergent sequences and is a constant, then
limnl an  L limxl fx  L n
3 limxl fx  L fn  an n
limnl an  L
FIGURE 6 2 0 x
y
1 3 4
L
y=ƒ
limxl 1xr
  0 r  0
4 lim
nl
1
nr  0 r  0
an limn l  an  
limnl  an   M
N
n  N an  M
limn l  an   an 
an  
5
an  bn  c
lim
nl
an  bn   lim
nl
an  lim
nl
bn
lim
nl
an  bn   lim
nl
an  lim
nl
bn
lim
nl
can  c lim
nl
an lim
nl
c  c
lim
nl
an bn   lim
nl
an  lim
nl
bn
lim
nl
an
bn

lim
n l 
an
lim
nl
bn
if limnl
bn  0
lim
nl
an
p  
lim
nl
an
p
if p  0 and an  0
Limit Laws for Sequences
97909_11_ch11_p689-697.qk_97909_11_chRights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
694 CHAPTER 11 INFINITE SEQUENCES AND SERIES
The Squeeze Theorem can also be adapted for sequences as follows (see Figure 7).
If for and , then .
Another useful fact about limits of sequences is given by the following theorem, whose
proof is left as Exercise 87.
Theorem If , then .
Find .
SOLUTION The method is similar to the one we used in Section 2.6: Divide numerator
and denominator by the highest power of that occurs in the denominator and then use
the Limit Laws.
Here we used Equation 4 with .
Is the sequence convergent or divergent?
SOLUTION As in Example 4, we divide numerator and denominator by :
because the numerator is constant and the denominator approaches . So is
divergent.
Calculate .
SOLUTION Notice that both numerator and denominator approach infinity as . We
can’t apply l’Hospital’s Rule directly because it applies not to sequences but to functions
of a real variable. However, we can apply l’Hospital’s Rule to the related function
and obtain
Therefore, by Theorem 3, we have
an 
 bn 
 cn n  n0 lim
n l 
an  lim
n l 
cn  L lim
nl 
bn  L
6 lim
nl 	 an 	  0 limnl
an  0
lim
nl
n
n  1
n
lim
nl
n
n  1  lim
nl
1
1
1
n

lim
nl
1
lim
nl
1  lim
nl
1
n
 1
1  0  1
r  1
EXAMPLE 4
EXAMPLE 5 an  n
s10  n
n
lim
nl
n
s10  n  lim
nl
1
 10
n2
1
n
 
0 an
lim
nl 
ln n
n
n l 
EXAMPLE 6
fx  ln xx
lim
xl 
ln x
x  lim
xl 
1x
1  0
lim
nl 
ln n
n  0
Squeeze Theorem for Sequences
FIGURE 7
The sequence b  is squeezed
between the sequences a 
and c .
0 n
cn
an
bn
n
n
n
This shows that the guess we made earlier
from Figures 1 and 2 was correct.
97909_11_ch11_p689-697.qk_979ng. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
SECTION 11.1 SEQUENCES 695
Determine whether the sequence is convergent or divergent.
SOLUTION If we write out the terms of the sequence, we obtain
The graph of this sequence is shown in Figure 8. Since the terms oscillate between 1 and
infinitely often, does not approach any number. Thus does not exist;
that is, the sequence is divergent.
Evaluate if it exists.
SOLUTION We first calculate the limit of the absolute value:
Therefore, by Theorem 6,
The following theorem says that if we apply a continuous function to the terms of a convergent sequence, the result is also convergent. The proof is left as Exercise 88.
Theorem If and the function is continuous at , then
Find .
SOLUTION Because the sine function is continuous at , Theorem 7 enables us to write
Discuss the convergence of the sequence , where
.
SOLUTION Both numerator and denominator approach infinity as but here we
have no corresponding function for use with l’Hospital’s Rule ( is not defined when
is not an integer). Let’s write out a few terms to get a feeling for what happens to
as gets large:
It appears from these expressions and the graph in Figure 10 that the terms are decreasing
and perhaps approach 0. To confirm this, observe from Equation 8 that
an  1
n
1, 1, 1, 1, 1, 1, 1, . . .
1 an limn l  1
n
1
n 
EXAMPLE 7
lim
n l 
1
n
n
lim
n l   1
n
n   lim
n l 
1
n  0
lim
n l 
1
n
n  0
EXAMPLE 8
7 lim
nl
an  LfL
lim
nl
fan  fL
lim
nl
sinn
0
lim
nl
sinn  sinlim
nl
n  sin 0  0
EXAMPLE 9
an  n!nn
n!  1  2  3    n
n l 
x!
x an
v EXAMPLE 10
n
a3  1  2  3
3  3  3
a2  1  2
2  2
a1  1
an  1  2  3    n
n  n  n    n
8
an  1
n 
2  3    n
n  n    n 
0 n
an
1
1
2 3 4
_1
FIGURE 8
The graph of the sequence in Example 8 is
shown in Figure 9 and supports our answer.
FIGURE 9
0 n
an
1
1
_1
Creating Graphs of Sequences
Some computer algebra systems have special
commands that enable us to create sequences
and graph them directly. With most graphing
calcula tors, however, sequences can be
graphed by using parametric equations. For
instance, the sequence in Example 10 can be
graphed by entering the parametric equations
and graphing in dot mode, starting with
and setting the -step equal to . The result is
shown in Figure 10.
t 1
t  1
x  t y  t!tt
FIGURE 10
1
0 10
97909_11_ch11_p689-697.qk_97909_11_ch11_p689-697 9/22/10 10:34 AM Page 695
nned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
696 CHAPTER 11 INFINITE SEQUENCES AND SERIES
Notice that the expression in parentheses is at most 1 because the numerator is less than
(or equal to) the denominator. So
We know that as . Therefore as by the Squeeze Theorem.
For what values of is the sequence convergent?
SOLUTION We know from Section 2.6 and the graphs of the exponential functions in
Section 1.5 that for and for . Therefore,
putting and using Theorem 3, we have
It is obvious that
and
If , then , so
and therefore by Theorem 6. If , then diverges as in
Example 7. Figure 11 shows the graphs for various values of . (The case is
shown in Figure 8.)
The results of Example 11 are summarized for future use as follows.
The sequence is convergent if and divergent for all other
values of .
Definition A sequence is called increasing if for all ,
that is, It is called decreasing if for all .
A sequence is monotonic if it is either increasing or decreasing.
0 	 an 

1
n
1n l 0 n l  an l 0 n l 
r r n 
limxl  ax   a  1 limxl  ax  0 0 	 a 	 1
a  r
lim
n l 
r n  

0
if r  1
if 0 	 r 	 1
lim
nl
1n  1 lim
nl
0n  0
1 	 r 	 0 0 	 	r	 	 1
lim
n l  	r n
	  lim
n l  	r	
n  0
limn l  r n  0 r 
 1 r n 
r r  1
r>1
r=1
0<r<1
0
r<_1
_1<r<0
0 n
an
1
1
n
an
1
1
FIGURE 11
The sequence an=r n
v EXAMPLE 11
r 1 	 r 
 1 n 9 
r
lim
n l 
r n  
0
1
if 1 	 r 	 1
if r  1
10 an 
a1 	 a2 	 a3 	  .
an 	 an1 n  1
an  an1 n  1
97909_11_ch11_p689-age Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
SECTION 11.1 SEQUENCES 697
The sequence is decreasing because
and so for all .
Show that the sequence is decreasing.
SOLUTION 1 We must show that , that is,
This inequality is equivalent to the one we get by cross-multiplication:
Since , we know that the inequality is true. Therefore and
so is decreasing.
SOLUTION 2 Consider the function :
Thus is decreasing on and so . Therefore is decreasing.
Definition A sequence is bounded above if there is a number such that
It is bounded below if there is a number such that
If it is bounded above and below, then is a bounded sequence.
For instance, the sequence is bounded below but not above. The
sequence is bounded because for all .
We know that not every bounded sequence is convergent [for instance, the sequence
satisfies but is divergent from Example 7] and not every mono -
 3
n  5 
3
n  5

3
n  1  5  3
n  6
an  an1 n  1
EXAMPLE 12
an  n
n2  1
an1 	 an
n  1
n  1
2  1
	
n
n2  1
n  1
n  1
2  1
	
n
n2  1 &? n  1n2  1 	 nn  1
2  1
&? n3  n2  n  1 	 n3  2n2  2n
&? 1 	 n2  n
n  1 n2  n  1 an1 	 an
an 
fx  x
x 2  1
fx  x 2  1  2x 2
x 2  1
2  1  x 2
x 2  1
2 	 0 whenever x 2  1
f 1,  fn  fn  1 an 
EXAMPLE 13
an  M
an 
 M for all n  1
m
m 
 an for all n  1
an 
11
an  n an  0
an  nn  1 0 	 an 	 1 n
an  1
n 1 
 an 
 1
The right side is smaller because it has a
larger denominator.
97909_11_ch11_p689-697.qk_97909_11_ch11_p689-697 9/22/10 10:34 AM Page 697
Coed, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
698 CHAPTER 11 INFINITE SEQUENCES AND SERIES
tonic sequence is convergent . But if a sequence is both bounded and
monotonic, then it must be convergent. This fact is proved as Theorem 12, but intuitively
you can understand why it is true by looking at Figure 12. If is increasing and
for all , then the terms are forced to crowd together and approach some number .
The proof of Theorem 12 is based on the Completeness Axiom for the set of real
numbers, which says that if is a nonempty set of real numbers that has an upper bound
( for all in ), then has a least upper bound . (This means that is an upper
bound for , but if is any other upper bound, then .) The Completeness Axiom is
an expression of the fact that there is no gap or hole in the real number line.
Monotonic Sequence Theorem Every bounded, monotonic sequence is
convergent.
PROOF Suppose is an increasing sequence. Since is bounded, the set
has an upper bound. By the Completeness Axiom it has a least upper
bound . Given , is not an upper bound for (since is the least upper
bound). Therefore
But the sequence is increasing so for every . Thus if , we have
so
since . Thus
so .
A similar proof (using the greatest lower bound) works if is decreasing.
The proof of Theorem 12 shows that a sequence that is increasing and bounded above is
convergent. (Likewise, a decreasing sequence that is bounded below is convergent.) This
fact is used many times in dealing with infinite series.
an  n l
an  an  M
n L

S M
x  M xS S b b
S M b  M
12
an  an 
S  an  n  1
L   0 L   S L
aN  L   for some integer N
an  aN n  N n  N
an  L  
0  L  an  
an  L
 L  an    whenever n  N
limn l  an  L
an 
FIGURE 12
0 2 n
an
1 3
L
M
97909_11_ch110 Cengage Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s).
Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it.
SECTION 11.1 SEQUENCES 699
Investigate the sequence defined by the recurrence relation
SOLUTION We begin by computing the first several terms:
These initial terms suggest that the sequence is increasing and the terms are approaching
6. To confirm that the sequence is increasing, we use mathematical induction to show
that for all . This is true for because . If we assume
that it is true for , then we have
so
and
Thus
We have deduced that is true for . Therefore the inequality is true
for all by induction.
Next we verify that is bounded by showing that for all . (Since the
sequence is increasing, we already know that it has a lower bound: for
all .) We know that , so the assertion is true for . Suppose it is true for
. Then
so
and
Thus
This shows, by mathematical induction, that for all .
Since the sequence is increasing and bounded, Theorem 12 guarantees that it has
a limit. The theorem doesn’t tell us what the value of the limit is. But now that we know
exists, we can use the given recurrence relation to write
Since , it follows that too (as , also). So we have
Solving this equation for , we get , as we predicted."""