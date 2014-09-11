#curl demonstration
import commands

co = 'curl  -i --data "message=L\'enfant qui voulait etre un ours"  http://www.cs.odu.edu/~anwala/files/CS895Assignment1/problem1_CS895Assignment1form.php > problem1_curlDemonstrationOutput.html'
data = commands.getoutput(co)

print data