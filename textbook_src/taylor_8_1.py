


text = """In this chapter, I shall discuss the motion of two bodies each of which exerts a
conservative, central force on the other but which are subject to no other, "external,"
forces. There are many examples of this problem: the two stars of a binary star system,
a planet orbiting the sun, the moon orbiting the earth, the electron and proton in a
hydrogen atom, the two atoms of a diatomic molecule. In most cases the true situation
is more complicated. For example, even if we are interested in just one planet orbiting
the sun, we cannot completely neglect the effects of all the other planets; likewise,
the moon—earth system is subject to the external force of the sun. Nevertheless, in all
cases, it is an excellent starting approximation to treat the two bodies of interest as
being isolated from all outside influences.
You may also object that the examples of the hydrogen atom and the diatomic
molecule do not belong in classical mechanics, since all such atomic-scale systems
must really be treated by quantum mechanics. However, many of the ideas I shall
develop in this chapter (the important idea of reduced mass, for instance) play a crucial
role in the quantum mechanical two-body problem, and it is probably fair to say that
the material covered here is an essential prerequisite for the corresponding quantum
material.
8.1 The Problem
Let us consider two objects, with masses m iand m2 . For the purposes of this chapter,
I shall assume the objects are small enough to be considered as point particles, whose
positions (relative to the origin 0 of some inertial reference frame) I shall denote
by r1and r2 . The only forces are the forces F12 and F21 of their mutual interaction,
which I shall assume is conservative and central. Thus the forces can be derived from
a potential energy U(ri , r2 ). In the case of two astronomical bodies (the earth and
293 
294 Chapter 8 Two-Body Central-Force Problems
the sun, for instance) the force is the gravitational force Gm 01 211r 1 — r2 1 2 , with the
corresponding potential energy (as we saw in Chapter 4)
Gm im2
U(r1, r2 ) = .
1ri— r2 1 (8.1)
For the electron and proton in a hydrogen atom, the potential energy is the Coulomb
PE of the two charges (e for the proton and —e for the electron),
ke 2
U(r1, r2 ) = , , (8.2)
Iri— r2 1
where k denotes the Coulomb force constant, k = 1/47rEo .
In both of these examples, U depends only on the difference (r 1— r2), not on
r 1and r2separately. As we saw in Section 4.9, this is no accident: Any isolated
system is translationally invariant, and if U(r i , r2) is translationally invariant it can
only depend on (r 1— r2). In the present case there is a further simplification: As we
saw in Section 4.8, if a conservative force is central, then U is independent of the
direction of (r 1— r2 ). That is, it only depends on the magnitude 11. 1 — r2 1, and we can
write
U(r1, r2 ) = U(1r 1 — r2 1) (8.3)
as is the case in the examples (8.1) and (8.2).
To take advantage of the property (8.3), it is convenient to introduce the new
variable
r = r 1— r2 . (8.4)
As shown in Figure 8.1, this is just the position of body 1 relative to body 2, and
I shall refer to r as the relative position. The result of the previous paragraph can be
rephrased to say that the potential energy U depends only on the magnitude r of the
relative position r,
U = U (r). (8.5)
Figure 8.1 The relative position r = r 1— r2is the position
of body 1 relative to body 2. 
Section 8.2 CM and Relative Coordinates; Reduced Mass 295
We can now state the mathematical problem that we have to solve: We want to
find the possible motions of two bodies (the moon and the earth, or an electron and a
proton), whose Lagrangian is
= 1m2q: — U(r). (8.6)
Of course, I could equally have stated the problem in Newtonian terms, and I shall
in fact feel free to move back and forth between the Lagrangian and Newtonian
formalisms according to which seems the more convenient. For the present, the
Lagrangian formalism is the more transparent. """
