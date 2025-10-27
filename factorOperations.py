# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors: List[Factor]):
    """
   输入因子是因子的列表。
   
您应该计算无条件变量和条件变量集
    变量来连接这些因子。

返回一个具有这些变量及其概率条目的新因子
    是输入因子的相应行的乘积。

您可以假设所有输入的 variableDomainsDict
    因子是相同的，因为它们来自同一个贝叶斯网。

joinFactors 将只允许 unconditionedVariables 出现在
    一个输入因子（因此它们的连接是明确定义的）。

提示：将 assignmentDict 作为输入的因子方法
    （如 getProbability 和 setProbability）可以处理
    assignmentDicts，分配的变量多于该因子中的变量。

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors] # list of sets, where each set is a factor's unconditionedVariables
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"
    all_unconditioned_variables = set()
    all_conditioned_variables = set()
    var_domains=None
    for factor in factors:
        if var_domains == None:
            var_domains = factor.variableDomainsDict()
        all_unconditioned_variables.update(factor.unconditionedVariables())
        all_conditioned_variables.update(factor.conditionedVariables())
        
    all_conditioned_variables = all_conditioned_variables - all_unconditioned_variables #减去交集
    
    new_factor = Factor(list(all_unconditioned_variables), list(all_conditioned_variables), var_domains)
    for assignment_dict in new_factor.getAllPossibleAssignmentDicts():
        probability = 1.0
        for factor in factors:
            probability *= factor.getProbability(assignment_dict)
        
        new_factor.setProbability(assignment_dict, probability)
        
    return new_factor
   
    
    
    "*** END YOUR CODE HERE ***"

########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        输入因子是单一因子。
        输入消除变量是要从因子中消除的变量。
        eliminationVariable 必须是因子中的无条件变量。
        
您应该计算无条件变量和条件变量集
        通过消除变量获得的因子的变量
        eliminationVariable 中。

返回一个新因素，其中所有行都提到
        eliminationVariable 与匹配的行相加
        赋值。
        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        factor_unconditioned_variables = factor.unconditionedVariables() - {eliminationVariable}
        factor_conditioned_variables = factor.conditionedVariables() - {eliminationVariable}
        
        new_factor = Factor(factor_unconditioned_variables, factor_conditioned_variables, factor.variableDomainsDict())
        
        elim_domain = factor.variableDomainsDict()[eliminationVariable]
        for assignment_dict in new_factor.getAllPossibleAssignmentDicts():
            probability = 0.0
            for domain_value in elim_domain:
                full_assignment_dict = assignment_dict.copy()
                full_assignment_dict[eliminationVariable] = domain_value
                probability += factor.getProbability(full_assignment_dict)
            new_factor.setProbability(assignment_dict, probability)
        
        return new_factor
        "*** END YOUR CODE HERE ***"

    return eliminate

eliminate = eliminateWithCallTracking()

