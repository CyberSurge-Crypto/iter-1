# Iteration 1 - Application layer (backend)

## Transaction Part

### Transaction State

- STARTED - means that the transaction started, but not signed

- SIGNED - means that the transaction was signed, but not broadcasted

- PENDING - means that the transaction was broadcasted, but waiting for confirmation

- FIRST_CONFIRMED - means that the transaction is uploaded to the first block. But this block is still likely to be dismissed if there are other blocks in the same height, so it is called first confirmed.

- FULLY_CONFIRMED - means that the transaction stays in a block with 5 consequent blocks, which indicates a very high likelihood that it would not be dismissed. Hence, this state is called fully confirmed.

- CANCELED - means that the transaction is canceled due to dismissing.

- FAILED - means that the transaction did not pass the verification or validation.

## Lifecycle

The state is changed according to the chart: [Google Draw Chart](https://docs.google.com/drawings/d/1oHp5yySXUYxn5rJKT0gWFaxbh7SpsEF2ng5gvG_ls-Y/edit?usp=sharing)

## Test Cases