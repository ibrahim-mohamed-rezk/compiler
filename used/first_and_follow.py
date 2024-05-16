def handle():
    global start_symbol, rules, nonterm_userdef,\
        term_userdef, diction, firsts, follows

    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs
    print(f"\nRules: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")


def computeAllFirsts():
    global start_symbol, rules, nonterm_userdef,\
        term_userdef, diction, firsts, follows

    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        firsts[y] = t

    print("\nCalculated firsts: ")
    for y in firsts:
        print(f"first({y}) => {firsts[y]}")


def first(sub_rules):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    if len(sub_rules) != 0 and (sub_rules is not None):
        if sub_rules[0] in term_userdef:
            return sub_rules[0]
        elif sub_rules[0] == 'ε':
            return 'ε'
    if len(sub_rules) != 0:
        if sub_rules[0] in list(diction.keys()):
            fres = []
            rhs_rules = diction[sub_rules[0]]
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            if 'ε' not in fres:
                return fres
            else:
                newList = []
                fres.remove('ε')
                if len(sub_rules) > 1:
                    ansNew = first(sub_rules[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                fres.append('ε')
                return fres


def follow(sub_rules):
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    solset = set()
    if sub_rules == start_symbol:
        solset.add('$')
    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            if sub_rules in subrule:
                while sub_rules in subrule:
                    index_nt = subrule.index(sub_rules)
                    subrule = subrule[index_nt + 1:]
                    if len(subrule) != 0:
                        res = first(subrule)
                        if 'ε' in res:
                            newList = []
                            res.remove('ε')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        if sub_rules != curNT:
                            res = follow(curNT)
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef,\
        term_userdef, diction, firsts, follows
    for sub in diction:
        solset = set()
        sol = follow(sub)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[sub] = solset

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1


def ParseTable():
    global diction, firsts, follows, term_userdef
    
    ntlist = list(diction.keys())
    terminals = term_userdef.copy()
    terminals.append('$')

    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        mat.append(row)

    grammar_is_LL = True

    for lhs in diction.keys():
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)

            if 'ε' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('ε')
                    res = list(res) + list(follows[lhs])
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = ttemp.copy()
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] + f"{lhs} -> {' '.join(y)}"
                else:
                    if f"{lhs} -> {y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] + f",{lhs} -> {' '.join(y)}"

    print("\nGenerated parsing table:\n")
    frmt = "{:>13} |" * len(terminals)
    print("-----------------------------------------------------------------------------------------------------------------------------")
    print(frmt.format(*terminals))

    j = 0
    for y in mat:
        frmt1 = "{:>12} | " * len(y)
        print("-----------------------------------------------------------------------------------------------------------------------------")
        print(f"{ntlist[j]}  | {frmt1.format(*y)}")
        j += 1

    return (mat, grammar_is_LL, terminals)



sample_input_string = None


rules = ["S -> A B C",
         "A -> k d | a | d C",
         "C -> c ",
         "B -> b B C | ε r"]

nonterm_userdef = ['A', 'B', 'C']
term_userdef = ['k', 'O', 'd', 'a', 'c', 'b', 'r']


diction = {}
firsts = {}
follows = {}

handle()
computeAllFirsts()
start_symbol = list(diction.keys())[0]
computeAllFollows()

(parsing_table, result, tabTerm) = ParseTable()
