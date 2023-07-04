import itertools,re
def parse_circuit_file(file_path):
    circuit = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                net, expression = line.strip().split('=')
                circuit[net.strip()] = expression.strip()
    return circuit

def parse_fault_file(file_path):
    fault={}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                net, expression = line.strip().split('=')
                fault[net.strip()] = expression.strip()
    return fault
def bitwise_eval(expression):
    operators = {
        '&': lambda x, y: x & y,
        '|': lambda x, y: x | y,
        '^': lambda x, y: x ^ y,
        '~': lambda x: 0 if x=='1' else 1
    }

    stack = []
    expression=expression.split()
    i=0
    while i < len(expression):
        token=expression[i]
        if token.isdigit():
            stack.append(int(token))
            i=i+1
        elif token in operators:
            if token == '~':
                operand = expression[i+1]
                i=i+2
                result = operators['~'](operand)
                stack.append(result)
            else:
                operand2 = int(expression[i+1])
                i=i+2
                operand1 = int(stack.pop())
                result = operators[token](operand1, operand2)
                stack.append(result)

    return stack.pop()

def evaluate_expression(expression, input_vector):
    for variable, value in input_vector.items():
        expression = expression.replace(variable, str(value))
    ans=bitwise_eval(expression)
    return ans

def evaluate_correct_output(circuit,input_vector,output_variable):
  expression=circuit[output_variable]
  for i in expression:
    if i in ['|', '^','~','&']:
        expression = expression.replace(i, ' ')
  expression=expression.split()

  for exp_item in expression:
    if exp_item.strip() not in input_vector:
      input_vector[exp_item.strip()]=evaluate_correct_output(circuit,input_vector,exp_item.strip())

  return evaluate_expression(circuit[output_variable],input_vector)

def evaluate_wrong_output(circuit,input_vector,output_variable,fault_location,fault_value):
  input=input_vector
  input[fault_location]=fault_value
  return evaluate_correct_output(circuit,input,output_variable)

def main():
    circuit_file = "circuit.txt"
    circuit = parse_circuit_file(circuit_file)

    fault=parse_fault_file("fault.txt")
    fault_location = fault['FAULT_AT']
    fault_type=fault['FAULT_TYPE']
    faul='0'
    if fault_type.strip() == "SA1":
        faul='1'
    all_input_combinations = list(itertools.product([0, 1], repeat=4))

    test_results = []
    for input_combination in all_input_combinations:
        input_vector_1 = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        input_vector_2={'A': 0, 'B': 0, 'C': 0, 'D': 0}

        input_vector_1.update(dict(zip(['A', 'B', 'C', 'D'], input_combination)))
        
        z=evaluate_correct_output(circuit,input_vector_1,"Z")

        input_vector_2.update(dict(zip(['A', 'B', 'C', 'D'], input_combination)))

        z_=evaluate_wrong_output(circuit,input_vector_2,"Z",fault_location,faul)
        
        if z!=z_:
          test_results.append((input_vector_1,z,z_))

    with open("output.txt", 'w') as output_file:
       for input_vector, correct_out,faulty_out in test_results:
          input=[]
          input.append(input_vector['A'])
          input.append(input_vector['B'])
          input.append(input_vector['C'])
          input.append(input_vector['D'])
          output_file.write(f"[A,B,C,D]={input},Z={faulty_out}\n")
          # print(f"[A,B,C,D]={input},Z={faulty_out}\n")

if __name__=='__main__':
  main()
