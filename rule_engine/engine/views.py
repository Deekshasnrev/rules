from django.shortcuts import render
from .forms import RuleForm
from .models import ASTNode
from collections import Counter
import re
from django.core.exceptions import ValidationError
import json

# Define valid attributes and operators
VALID_ATTRIBUTES = ['age', 'department', 'salary', 'experience']
VALID_OPERATORS = ['>', '<', '=']


# Function to parse the rule string into an AST with proper handling of parentheses and logical operators
def parse_rule_string(rule_string):
    tokens = re.findall(r"\w+|[><=]+|\(|\)|'[^']*'|AND|OR", rule_string)

    def build_expression(tokens):
        root = build_ast(tokens)
        while tokens:
            operator = tokens.pop(0)
            if operator not in ['AND', 'OR']:
                raise ValidationError(f"Invalid logical operator: {operator}")
            right_node = build_ast(tokens)
            root = ASTNode.objects.create(
                node_type='operator',
                value=operator,
                left_child=root,
                right_child=right_node
            )
        return root

    def build_ast(tokens):
        if not tokens:
            return None
        
        token = tokens.pop(0)

        if token == '(':
            left_node = build_ast(tokens)
            if not tokens:
                raise ValidationError("Invalid rule format: Missing operator.")
            operator = tokens.pop(0)
            if operator not in ['AND', 'OR']:
                raise ValidationError(f"Invalid operator: {operator}")
            right_node = build_ast(tokens)
            if not tokens or tokens[0] != ')':
                raise ValidationError("Invalid rule format: Mismatched parentheses.")
            tokens.pop(0)  # Remove closing ')'
            node = ASTNode.objects.create(
                node_type='operator', 
                value=operator, 
                left_child=left_node, 
                right_child=right_node,
                is_root=False  # Not root here
            )
            return node
        else:
            if token in VALID_ATTRIBUTES:
                if not tokens:
                    raise ValidationError("Invalid comparison format: Missing operator or value.")
                operator = tokens.pop(0)
                if operator not in VALID_OPERATORS:
                    raise ValidationError(f"Invalid operator in comparison: {operator}")
                if not tokens:
                    raise ValidationError("Invalid comparison format: Missing value.")
                value = tokens.pop(0)
                node = ASTNode.objects.create(
                    node_type='operand', 
                    value=f"{token} {operator} {value}",
                    is_root=False  # Not root here
                )
                return node
            else:
                raise ValidationError(f"Invalid comparison format: {token}")
    
    # Build the root AST node and mark it as root
    ast_root = build_expression(tokens)
    ast_root.is_root = True  # Mark this as the root node
    ast_root.save()  # Save the change to the database
    return ast_root



# Function to combine multiple rules into a single AST
def find_most_frequent_operator(rules):
    # Count occurrences of logical operators ('AND' or 'OR') in the rules
    operator_count = Counter()
    
    for rule in rules:
        # Using regex to find all occurrences of AND/OR
        operator_count.update(re.findall(r'\b(AND|OR)\b', rule))
    
    # Return the most frequent operator, or 'OR' by default if none found
    return operator_count.most_common(1)[0][0] if operator_count else 'OR'


def combine_rules(rules):
    # Parse each rule into its own AST
    ast_roots = [parse_rule_string(rule) for rule in rules]
    
    if not ast_roots:
        return None

    # Use the most frequent operator heuristic to decide how to combine ASTs
    frequent_operator = find_most_frequent_operator(rules)
    
    # Initialize the combined AST with the first rule's AST
    combined_ast = ast_roots[0]
    
    # Avoid duplicate conditions in the combined AST
    added_conditions = set()

    # Recursively add each AST to the combined tree
    for ast in ast_roots[1:]:
        if ast.value not in added_conditions and ast.value not in VALID_OPERATORS:
            combined_ast = ASTNode.objects.create(
                node_type='operator',
                value=frequent_operator,  # Use the most frequent operator
                left_child=combined_ast,
                right_child=ast
            )
            # Add conditions to prevent duplication
            added_conditions.add(ast.value)
    
    return combined_ast


# Function to evaluate the AST against input data
def evaluate_rule(ast_node, data):
    if ast_node.node_type == 'operand':
        # Parse the operand and check the data
        field, operator, value = ast_node.value.split()  # e.g., "age > 30"
        value = int(value) if value.isdigit() else value.strip("'")
        
        # Compare based on the operator
        if operator == '>':
            return data[field] > value
        elif operator == '<':
            return data[field] < value
        elif operator == '=':
            return data[field] == value
    else:
        # Logical operator (AND/OR)
        left_result = evaluate_rule(ast_node.left_child, data)
        right_result = evaluate_rule(ast_node.right_child, data)
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result


# View to handle rule creation via the form
def create_rule_view(request):
    form = RuleForm()
    error_message = None
    
    # Clear the database (remove all rules) every time the server starts
    if request.method == 'GET':  # Only clear when accessing the page initially
        ASTNode.objects.all().delete()
    
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            rule_string = form.cleaned_data['rule_string']
            try:
                ast_root = parse_rule_string(rule_string)
                ast_representation = traverse_ast(ast_root)  # Get the full AST as a string
                
                # Save the newly created rule
                root_nodes = ASTNode.objects.all()  # Show all created root nodes including newly created ones
                
                return render(request, 'engine/create_rule.html', {
                    'form': form,
                    'ast_representation': ast_representation,
                    'root_nodes': root_nodes,
                    'error_message': error_message
                })
            except ValidationError as e:
                error_message = e.messages  # Catch validation errors and pass to the template

    root_nodes = ASTNode.objects.all()
    return render(request, 'engine/create_rule.html', {'form': form, 'error_message': error_message})



def list_rules_view(request):
    # Fetch nodes that do not have a parent (are not a left or right child)
    root_nodes = ASTNode.objects.filter(is_root=True)
    return render(request, 'engine/rule_list.html', {'root_nodes': root_nodes})


# View to handle the combination of multiple rules
def combine_rules_view(request):
    combined_ast_representation = None
    error_message = None
    combined_rules = []

    if request.method == 'POST':
        rules = request.POST.get('rules', '').splitlines()  # Split the input into lines

        # Remove any empty lines
        rules = [rule.strip() for rule in rules if rule.strip()]

        try:
            combined_ast_root = combine_rules_by_pattern(rules)
            combined_ast_representation = traverse_ast(combined_ast_root)  # Get the full AST as a string
            combined_rules.append(combined_ast_representation)  # Show the combined rule as a string
        except ValidationError as e:
            error_message = e.messages
        except Exception as e:
            error_message = "Invalid form input."

    # Fetch all previously combined rules that have operators as root nodes
    all_combined_rules = ASTNode.objects.filter(node_type='operator').all()

    # Traverse and convert each ASTNode into a readable string
    combined_rules_list = [traverse_ast(rule) for rule in all_combined_rules]

    return render(request, 'engine/combine_rules.html', {
        'combined_ast_representation': combined_ast_representation,
        'combined_rules': combined_rules_list,  # Use the list of combined rule strings
        'error_message': error_message,
    })

def create_operator_node(operator, left_child, right_child):
    """Creates an operator node for the AST."""
    return ASTNode.objects.create(
        node_type='operator',
        value=operator,
        left_child=left_child,
        right_child=right_child
    )


def combine_rules_by_pattern(rules):
    """Combines rules based on the pattern provided."""
    num_rules = len(rules)

    # Find the most frequent operator from the list of rules
    frequent_operator = find_most_frequent_operator(rules)

    if num_rules == 1:
        # Single rule, just parse and return it
        return parse_rule_string(rules[0])

    if num_rules == 2:
        # Combine the two rules directly with the frequent operator
        left_node = parse_rule_string(rules[0])
        right_node = parse_rule_string(rules[1])
        return create_operator_node(frequent_operator, left_node, right_node)

    if num_rules == 3:
        # Combine the first two as left and third as right
        left_node = combine_rules_by_pattern(rules[:2])
        right_node = parse_rule_string(rules[2])
        return create_operator_node(frequent_operator, left_node, right_node)

    if num_rules == 4:
        # Combine the first two as left and the last two as right
        left_node = combine_rules_by_pattern(rules[:2])
        right_node = combine_rules_by_pattern(rules[2:])
        return create_operator_node(frequent_operator, left_node, right_node)

    if num_rules == 5:
        # Combine the first three as left and the last two as right
        left_node = combine_rules_by_pattern(rules[:3])
        right_node = combine_rules_by_pattern(rules[3:])
        return create_operator_node(frequent_operator, left_node, right_node)

    # If more than 5, continue the pattern
    split_index = (num_rules + 1) // 2
    left_node = combine_rules_by_pattern(rules[:split_index])
    right_node = combine_rules_by_pattern(rules[split_index:])
    return create_operator_node(frequent_operator, left_node, right_node)





def evaluate_rule(ast_node, data):
    print(f"Evaluating node: {ast_node.node_type} - {ast_node.value}")
    
    if ast_node.node_type == 'operand':
        # Extract the operand and check the data
        parts = ast_node.value.split(maxsplit=2)  # Split only into three parts: field, operator, value
        
        if len(parts) != 3:
            raise ValueError(f"Invalid operand format: {ast_node.value}")
        
        field, operator, value = parts  # e.g., "age > 30"
        print(f"Checking condition: {field} {operator} {value}")
        
        # Convert the value to the appropriate type (int, float, or string)
        try:
            value = int(value) if value.isdigit() else float(value)
        except ValueError:
            value = value.strip("'").strip('"')  # Remove any quotes for string values
        
        # Compare based on the operator
        if field not in data:
            raise KeyError(f"Field '{field}' not found in data.")
        
        if operator == '>':
            result = data[field] > value
        elif operator == '<':
            result = data[field] < value
        elif operator == '=':
            result = data[field] == value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

        print(f"Result for {field} {operator} {value}: {result}")
        return result
    
    elif ast_node.node_type == 'operator':
        # Logical operator (AND/OR)
        left_result = evaluate_rule(ast_node.left_child, data)
        right_result = evaluate_rule(ast_node.right_child, data)
        print(f"Logical operator {ast_node.value} - Left: {left_result}, Right: {right_result}")
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unsupported logical operator: {ast_node.value}")
    else:
        raise ValueError(f"Unsupported node type: {ast_node.node_type}")



# View to handle evaluation of the rule

def evaluate_rule_view(request):
    error_message = None
    evaluation_result = None
    user_data_json = ""  # Initialize this variable at the beginning
    user_data = ""

    if request.method == 'POST':
        # Get user data JSON from the form
        user_data_json = request.POST.get('data')

        # Check if the data is not empty
        if user_data_json:
            try:
                # Parse the user data JSON into a Python dictionary
                user_data = json.loads(user_data_json)

                # Fetch the most recent AST node (update this function as per your logic)
                ast_node = fetch_latest_ast_node()  # Replace with your method to get the rule's AST node

                if ast_node is None:
                    error_message = "No rule available for evaluation."
                else:
                    # Evaluate the rule using the AST node and user data
                    evaluation_result = evaluate_rule(ast_node, user_data)

            except json.JSONDecodeError as e:
                error_message = f"Error in evaluation: {str(e)}"
            except KeyError as e:
                error_message = f"Field '{e.args[0]}' not found in data."
            except ValueError as e:
                error_message = f"Error in evaluation: {str(e)}"
            except Exception as e:
                error_message = f"Unexpected error: {str(e)}"
        else:
            error_message = "No user data provided."

    return render(request, 'engine/evaluate_rule.html', {
        'user_data': user_data_json or '',
        'evaluation_result': evaluation_result,
        'error_message': error_message
    })

# Helper function to traverse the AST and return a string representation
def traverse_ast(node):
    if node is None:
        return ""  # Or handle it in a more appropriate way
    
    if node.node_type == 'operator':
        left = traverse_ast(node.left_child)
        right = traverse_ast(node.right_child)
        return f"({left} {node.value} {right})"
    else:
        return f"{node.value}"


def fetch_latest_ast_node():
    return ASTNode.objects.last()  # Fetch the most recent AST node from the database


