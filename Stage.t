                // Lock state${Index}
                Monitor.Enter(states[${Index}], ref takenLocks[${Index}]);
                // Execute stage${Index}
                states[${Next}] = stage${Index}(${SharedState}(T${Index})(states[${Index}]));
                // Bail out if returned null
                if (states[${Next}] == null)
                {
                    return;
                }
