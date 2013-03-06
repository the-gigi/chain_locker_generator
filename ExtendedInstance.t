    public class ChainLockerEx<T, ${StateTypeList}>
${ClassConstraints}
    {
        T  _sharedState;
        public ChainLockerEx(T sharedState)
        {
            _sharedState = sharedState;
        }

        public void Do(T0 state0,
${Funcs},
                       Action<T, T${Last}>      stage${Last})
        {
            if (state0 == null)
            {
                throw new Exception("state0 can't be null");
            }

            var takenLocks = Enumerable.Repeat(false, ${Count}).ToArray();
            var states = Enumerable.Repeat<object>(null, ${Count}).ToArray();
            states[0] = state0;            
            try
            {
                Monitor.Enter(states[${Last}], ref takenLocks[${Last}]);
                // Execute stage1
                states[1] = stage1(_sharedState, (T0)state0));
                if (states[1] == null)
                {
                    return;
                }
${Stages}
                // Lock state${Last}
                Monitor.Enter(states[${Last}], ref takenLocks[${Last}]);
                // Release the state1 lock so other threads can work on it
                Monitor.Exit(states[${OneBeforeLast}]);
                takenLocks[${OneBeforeLast}] = false;
                // Execute stage${Last}
                stage${Last}(_sharedState, (T${Last})(states[${Last}]));
            }
            finally
            {
                // Release still held locks (If an exception was thrown)
                for (int i = 0; i < ${Count}; ++i)
                {
                    if (states[i] != null && takenLocks[i])
                    {
                        Monitor.Exit(states[i]);
                    }
                }
            }
        }
    }