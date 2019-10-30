from Parser import MyParser
parser = MyParser()
parsed_formula = parser('<(a & ~b); (~a & b)>(a & last) -> [(a)*; (b)]last'.replace(' ', ''))
print(parsed_formula)

def print_f(f):
	if f[0] == '&':
		return f'(({print_f(f[1])})&({print_f(f[2])}))'
	elif f[0] == '|':
		return f'(({print_f(f[1])})|({print_f(f[2])}))'
	elif f[0] == '~':
		return f'(~({print_f(f[1])}))'
	elif f[0] == '*':
		return f'(({print_f(f[1])})*)'
	elif f[0] == '?':
		return f'(({print_f(f[1])})?)'
	elif f[0] == '<>':
		return f'(<{print_f(f[1])}>({print_f(f[2])}))'
	elif f[0] == '[]':
		return f'([{print_f(f[1])}]({print_f(f[2])}))'
	elif f[0] == ';':
		return f'(({print_f(f[1])});({print_f(f[2])}))'
	else:
		return f'{f}'

def nnf(f): 
	if len(f) == 0:
		return f
	if f[0] == '~':
		if f[1][0] == '~':
			return nnf(f[1][1])
		elif f[1][0] == '&':
			return ('|', nnf(('~',f[1][1])), nnf(('~',f[1][2])))
		elif f[1][0] == '|':
			return ('&', nnf(('~',f[1][1])), nnf(('~',f[1][2])))
		elif f[1][0] == '<>':
			return ('[]', nnf(f[1][1]), nnf(('~',f[1][2])))
		elif f[1][0] == '[]':
			return ('<>', nnf(f[1][1]), nnf(('~',f[1][2])))
		else:
			return (f[0],) + tuple(map(nnf, f[1:]))
	else:
		if type(f) == tuple:
			return (f[0],) + tuple(map(nnf, f[1:]))
		else:
			return f

def prop_of_formula(f):
	if f[0] == '&':
		return ('&', re_formula(f[1]), re_formula(f[2]))
	elif f[0] == '|':
		return ('|', re_formula(f[1]), re_formula(f[2]))
	elif f[0] == '~':
		return ('~', re_formula(f[1]))
	elif type(f) != tuple:
		return f
	else:
		return None

#U = union
#I = intersection
def path(p):
	if p[0] == ';':
		return (';', path(p[1]), path(p[2]))
	elif p[0] == '+':
		return ('U', path(p[1]), path(p[2]))
	elif p[0] == '*':
		return ('*', path(p[1]))
	elif p[0] == '?':
		return ('?', re_formula(p[1]))
	else:
		return prop_of_formula(p)

def re_formula(f):
	if f[0] == '&':
		return ('I', re_formula(f[1]), re_formula(f[2]))
	elif f[0] == '|':
		return ('U', re_formula(f[1]), re_formula(f[2]))
	elif f[0] == '~':
		return ('~', re_formula(f[1]))
	elif f[0] == '<>':
		return ('<>', path(f[1]), re_formula(f[2]))
	elif f[0] == '[]':
		return ('[]', path(f[1]), re_formula(f[2]))
	else:  # atomic
		return prop_of_formula(f)

print(nnf(parsed_formula))
print(re_formula(nnf(parsed_formula)))

def newval(prefix):
	cont = 0:
	while  1:
		cont += 1
		yield f'{prefix}_{cont}'

def re2mso(r):
	p0 = newval('_p')
