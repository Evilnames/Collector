# Project Guidelines

## File Size & Structure
Keep all files small. Break logic into focused functions that compose upward — small helpers roll up into mid-level functions, which roll up into top-level systems. If a file is getting long, split it.

## Readability
Write systems that are easy to read and follow at a glance. Prefer clear naming and flat, obvious control flow over clever abstractions. A new reader should be able to understand any system quickly.

## Data Definitions
Keep data that needs to be modified in clearly defined, easy-to-find structures (dicts, lists, constants). Data should be easy to mutate — avoid scattering configuration or values across logic. Centralize definitions so changes require editing one place.
