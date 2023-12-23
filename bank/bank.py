# Prompt the user for a greeting and reward them based on it

greet = str(input('Greeting: '))

if greet.lower().strip().startswith('hello'):
    output = 0
elif greet.lower().strip().startswith('h'):
    output = 20
else:
    output = 100

print(f'${output}')