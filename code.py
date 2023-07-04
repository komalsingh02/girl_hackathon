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
def evaluate_expression(expression, input_vector):
    for variable, value in input_vector.items():
        expression = expression.replace(variable, str(value))
    return eval(expression)


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

    all_input_combinations = list(itertools.product([0, 1], repeat=4))

    test_results = []
    for input_combination in all_input_combinations:                                            
        input_vector = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

        input_vector.update(dict(zip(['A', 'B', 'C', 'D'], input_combination)))

        z=evaluate_correct_output(circuit,input_vector,"Z")
        
        input_vector.update(dict(zip(['A', 'B', 'C', 'D'], input_combination)))

        z_=evaluate_wrong_output(circuit,input_vector,"Z",fault_location,0)

        if z!=z_:
          test_results.append((input_vector,z,z_))

    with open("/content/output.txt", 'w') as output_file:
        for input_vector, correct_out,faulty_out in test_results:
            input=[]
            input.append(input_vector('A'))
            input.append(input_vector('B'))
            input.append(input_vector('C'))
            input.append(input_vector('D'))
            output_file.write(f"[A,B,C,D]={input},'Z'={faulty_out}\n")


if __name__=='__main__':
  main()