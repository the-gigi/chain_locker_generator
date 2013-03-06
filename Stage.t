                // Lock state${Index}
                Monitor.Enter(states[${Index}], ref takenLocks[${Index}]);
                // Release previous lock, so other threads can work on it
                Monitor.Exit(states[${Prev}]);
                takenLocks[${Prev}] = false;
                // Execute stage${Index}
                states[${Next}] = stage${Index}(${SharedState}(T${Index})(states[${Index}]));
                // Bail out if returned null
                if (states[${Next}] == null)
                {
                    return;
                }
