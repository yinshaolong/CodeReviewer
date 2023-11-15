function multiply(number1, number2) {
  // Convert inputs to numbers to avoid string concatenation or other type-related bugs
  const num1 = Number(number1);
  const num2 = Number(number2);
  
  // Check if the inputs are valid numbers
  if (isNaN(num1) || isNaN(num2)) {
    throw new Error('One or both inputs are not a valid number.');
  }
  
  return num1 * num2;
}

function main() {
  try {
    // Example usage with valid numeric string inputs
    console.log(multiply("3", "4"));
  } catch (error) {
    console.error(error.message);
  }
}

main();
