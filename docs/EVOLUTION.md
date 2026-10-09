# FinTalk.v Evolution Log

This file is maintained automatically by `scripts/daily_improve.py`, which runs
every 2 hours. Each entry records one autonomous improvement (or a reflection on
why none landed) plus the ideas queued for the next run. The AI reads the most
recent entries before deciding what to do, so this file is the project's memory.

Newest entries are at the bottom.

## 2026-09-16 03:27 UTC — Reflection: no code change landed
- **Attempted:** Add unit tests for RejectionDetector parsing logic
- **Blocked by:** rejected by gate: tests/test_rejection_detector.py failed: ---------------------------------------------------------------------- | Ran 11 tests in 0.001s | FAILED (failures=1)
- **Next:** Add tests for enhanced_core/conversation_manager.py pure helpers; Add tests for formula.py ratio calculations with edge cases (zero denominators); Harden rejection_detector: log at debug level for successful parses to reduce noise

## 2026-09-16 03:43 UTC — Add unit tests for ConversationManager pure logic
- **Type:** tests
- **Files:** tests/test_conversation_manager.py
- **Why:** The previous run's attempt at rejection_detector tests was rejected by the gate, and the evolution log explicitly suggests testing conversation_manager pure helpers next. ConversationManager has no heavy imports (only stdlib + logging), so its history/context/slot behaviour can be verified with the standard library unittest without network or API keys. These tests lock in current observable behaviour (turn ordering, maxlen trimming, entity dedup, clear() reset) so future refactors cannot silently break it.
- **Next:** Add tests for formula.py calculate_from_expression edge cases (division by zero, unknown variables, unsupported AST nodes) in tests/test_formula.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/correlation_checker.py keyword matching logic; Document ConversationManager context keys in API_REFERENCE.md

## 2026-09-16 08:58 UTC — Add unit tests for formula.py safe expression evaluation
- **Type:** tests
- **Files:** tests/test_formula.py
- **Why:** The evolution log's next ideas explicitly call for tests of formula.calculate_from_expression edge cases (division by zero, unknown variables, unsupported AST nodes). formula.py is pure stdlib + loguru, so it can be tested without network or heavy deps. These tests lock in the current safe-evaluation contract (NaN on unknown variables, NaN on division by zero, rejection of function calls/attribute access) so future refactors cannot silently weaken the sandbox.
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/correlation_checker.py keyword matching logic in tests/test_correlation_checker.py; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/arbitrator.py decision parsing in tests/test_arbitrator.py

## 2026-09-16 14:30 UTC — Reflection: no code change landed
- **Attempted:** Add unit tests for RejectionDetector parsing logic
- **Blocked by:** rejected by gate: tests/test_rejection_detector.py failed: FAIL: test_digit_embedded_in_text_is_parsed (tests.test_rejection_detector.TestRejectionDetectorParsing.test_digit_embedded_in_text_is_parsed) | self.assertFal
- **Next:** Add tests for enhanced_core/correlation_checker.py keyword matching logic in tests/test_correlation_checker.py; Add tests for enhanced_core/arbitrator.py decision parsing in tests/test_arbitrator.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md

## 2026-09-16 19:16 UTC — Add unit tests for CorrelationChecker and QueryArbitrator
- **Type:** tests
- **Files:** tests/test_correlation_checker.py, tests/test_arbitrator.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/correlation_checker.py and enhanced_core/arbitrator.py as next ideas, and both modules are pure stdlib (logging + dataclasses) with an injected llm_caller, so they can be tested without network or heavy deps. These tests lock in the observable parsing contract (empty input short-circuits, 'yes'/'no' prefix matching, unexpected responses default to False, arbitration letter mapping and fallback to 'A' on bad/None output) so future refactors cannot silently change behaviour.
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/rejection_detector.py parsing (note: previous attempts failed on the digit-embedded-in-text case; verify regex \b([01])\b behaviour before asserting); Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/query_rewriter.py prompt construction in tests/test_query_rewriter.py

## 2026-09-16 22:32 UTC — Reflection: no code change landed
- **Attempted:** Add unit tests for rejection_detector parsing logic
- **Blocked by:** rejected by gate: tests/test_rejection_detector.py failed: ERROR: test_empty_llm_response_defaults_to_not_rejected (tests.test_rejection_detector.TestRejectionDetector.test_empty_llm_response_defaults_to_not_rejected) 
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/query_rewriter.py prompt construction in tests/test_query_rewriter.py; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py

## 2026-09-17 02:51 UTC — Add unit tests for QueryRewriter pure logic
- **Type:** tests
- **Files:** tests/test_query_rewriter.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/query_rewriter.py prompt construction as a next idea, and the module is pure stdlib (logging + typing) with an injected llm_caller, so it can be tested without network or heavy deps. Reading the implementation shows a duplicated _is_bad_rewrite definition (the second silently overrides the first) and clear observable contracts: empty/whitespace queries are returned stripped, missing history short-circuits, bad rewrites (empty or low character overlap) fall back to the original query, and good rewrites are stripped and returned. These t
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py; Remove the duplicated _is_bad_rewrite definition in enhanced_core/query_rewriter.py (second silently overrides first); Document ConversationManager context keys in API_REFERENCE.md

## 2026-09-17 09:04 UTC — Reflection: no code change landed
- **Attempted:** Remove duplicated _is_bad_rewrite in query_rewriter.py
- **Blocked by:** rejected by gate: edit 0: old == new (no-op)
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/streaming_nlg.py pure formatting helpers in tests/test_streaming_nlg.py

## 2026-09-17 14:34 UTC — Reflection: no code change landed
- **Attempted:** Remove unreachable duplicate return in _get_company_info
- **Blocked by:** rejected by gate: tests/test_function_registry.py failed: KeyError: 'company_name' | FAIL: test_executive_director_ratio (tests.test_function_registry.TestExecuteDispatch.test_executive_director_ratio) | self.assertEqu
- **Next:** Add tests for enhanced_core/streaming_nlg.py pure helpers (generate_answer input validation paths) in tests/test_streaming_nlg.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/parallel_executor.py result aggregation in tests/test_parallel_executor.py

## 2026-09-17 19:28 UTC — Fix timeout handling in ParallelExecutor.execute_parallel
- **Type:** bugfix
- **Files:** enhanced_core/parallel_executor.py
- **Why:** as_completed(future_to_task, timeout=timeout) raises concurrent.futures.TimeoutError when the overall timeout elapses, but the code only catches the builtin TimeoutError inside the per-future loop, so a timeout propagates out of execute_parallel and the 'ensure all tasks have results' backfill never runs. The same flaw exists in execute_parallel_with_callbacks. Wrapping the collection loop in try/except concurrent.futures.TimeoutError lets the existing backfill fill in the missing tasks, matching the documented contract that every task gets a TaskResult.
- **Next:** —

## 2026-09-17 22:34 UTC — Add unit tests for ParallelExecutor result aggregation
- **Type:** tests
- **Files:** tests/test_parallel_executor.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/parallel_executor.py result aggregation as a next idea, and the module is pure stdlib (logging, typing, concurrent.futures, dataclasses) so it can be tested without network or heavy deps. Reading the implementation shows clear observable contracts: empty task dict returns {}, non-callable values and non-positive timeout/max_workers raise ValueError, every submitted task gets a TaskResult even on timeout, exceptions are captured into TaskResult.error, and callbacks fire on success/error. These tests lock in that contract so future refac
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py; Add tests for enhanced_core/streaming_nlg.py pure formatting helpers in tests/test_streaming_nlg.py

## 2026-09-18 02:38 UTC — Reflection: no code change landed
- **Attempted:** Add unit tests for RejectionDetector parsing logic
- **Blocked by:** rejected by gate: tests/test_rejection_detector.py failed: FAIL: test_none_response_defaults_to_accept (tests.test_rejection_detector.TestRejectionDetectorParsing.test_none_response_defaults_to_accept) | self.assertTru
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py; Add tests for enhanced_core/streaming_nlg.py pure formatting helpers in tests/test_streaming_nlg.py

## 2026-09-18 08:39 UTC — Reflection: no code change landed
- **Attempted:** Add unit tests for RejectionDetector parsing logic
- **Blocked by:** rejected by gate: tests/test_rejection_detector.py failed: FAIL: test_none_response_defaults_to_accept (tests.test_rejection_detector.TestRejectionDetectorParsing.test_none_response_defaults_to_accept) | self.assertTru
- **Next:** Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py (note: previous attempt failed on KeyError 'company_name' and executive_director_ratio — verify _execute_sql column names before asserting); Add tests for enhanced_core/streaming_nlg.py pure formatting helpers in tests/test_streaming_nlg.py; Remove the unreachable duplicate return block after the first return in enhanced_core/function_registry.py _get_company_info

## 2026-09-18 14:01 UTC — Fix unparseable-response fallback in RejectionDetector
- **Type:** bugfix
- **Files:** enhanced_core/rejection_detector.py, tests/test_rejection_detector.py
- **Why:** When the LLM returns None or an empty string, 'result_str' is empty, so the regex match is skipped, but the heuristic block then does 'str(result).lower()' which yields the literal 'none' or '' — neither of which contains accept/reject keywords, so it falls through to the warning path. More importantly, the heuristic block re-stringifies the raw result instead of using the already-normalized 'result_str', and the previous gate failures show the parsing contract is fragile. Making the fallback explicit and logging at debug level for successful parses reduces log noise while keeping the safe def
- **Next:** Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py (verify _execute_sql column names before asserting on company_name/executive_director_ratio); Remove the unreachable duplicate return block after the first return in enhanced_core/function_registry.py _get_company_info; Add tests for enhanced_core/streaming_nlg.py generate_answer input validation paths in tests/test_streaming_nlg.py; Document ConversationManager context keys in API_REFERENCE.md

## 2026-09-18 18:46 UTC — Remove unreachable duplicate return in _get_company_info
- **Type:** bugfix
- **Files:** enhanced_core/function_registry.py
- **Why:** In enhanced_core/function_registry.py, _get_company_info returns immediately after the first 'if not result' guard, so the trailing 'if result:' block is dead code that can never execute. Removing it eliminates the misleading duplicate return path and makes the function's single exit contract obvious to future readers, without changing any observable behaviour.
- **Next:** Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py (verify _execute_sql column names before asserting on company_name/executive_director_ratio); Add tests for enhanced_core/streaming_nlg.py generate_answer input validation paths in tests/test_streaming_nlg.py; Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-18 22:08 UTC — Reflection: no code change landed
- **Attempted:** Add unit tests for FinancialFunctionRegistry dispatch
- **Blocked by:** rejected by gate: tests/test_function_registry.py failed: KeyError: 'company_name' | FAIL: test_executive_director_ratio (tests.test_function_registry.TestExecuteDispatch.test_executive_director_ratio) | self.assertEqu
- **Next:** Add tests for enhanced_core/streaming_nlg.py generate_answer input validation paths in tests/test_streaming_nlg.py (stub requests via sys.modules); Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/arbitrator.py decision parsing edge cases beyond the existing tests/test_arbitrator.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-19 02:37 UTC — Add unit tests for StreamingNLG input validation paths
- **Type:** tests
- **Files:** tests/test_streaming_nlg.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/streaming_nlg.py generate_answer input validation as a next idea. The validation branches (invalid/empty data, empty/invalid query) return before any network call, so they are pure and testable with the standard library by stubbing the 'requests' module via sys.modules. These tests lock in the guard contract so future refactors cannot silently start issuing HTTP requests for bad input.
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py (verify _execute_sql column names before asserting on company_name/executive_director_ratio); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/streaming_nlg.py generate_answer success path with a fake requests.post returning a choices payload

## 2026-09-19 08:26 UTC — Reflection: no code change landed
- **Attempted:** Add tests for StreamingNLG generate_answer success path
- **Blocked by:** rejected by gate: tests/test_streaming_nlg_answer.py failed: FAIL: test_large_data_is_truncated_in_prompt (tests.test_streaming_nlg_answer.TestGenerateAnswerSuccess.test_large_data_is_truncated_in_prompt) | self.assert
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py (verify _execute_sql column names before asserting on company_name/executive_director_ratio); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/arbitrator.py decision parsing edge cases beyond the existing tests/test_arbitrator.py

## 2026-09-19 13:37 UTC — Add tests for FinancialFunctionRegistry dispatch and helpers
- **Type:** tests
- **Files:** tests/test_function_registry.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/function_registry.py as a next idea, and two prior attempts were rejected by the gate because they asserted on column names that the module does not actually produce. Reading the implementation shows the real observable contracts: unknown function names return {'error': ...}, missing required parameters raise KeyError which execute() catches and converts to {'error': str(e)}, empty/whitespace company names short-circuit to None in _get_company_id, and _calculate_concentration sums parsed percentages while treating '/' and unparseable v
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/arbitrator.py decision parsing edge cases beyond the existing tests/test_arbitrator.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/streaming_nlg.py generate_answer success path with a fake requests.post returning a choices payload (verify truncation threshold before asserting)

## 2026-09-19 16:57 UTC — Add tests for QueryArbitrator parsing edge cases
- **Type:** tests
- **Files:** tests/test_arbitrator_parsing.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/arbitrator.py decision parsing edge cases as a next idea, and the module is pure stdlib (logging, typing, dataclasses) so it can be exercised with a fake llm_caller. Reading the implementation shows clear observable contracts: empty/whitespace queries short-circuit to 'invalid' with confidence 1.0 and never call the LLM; None or non-string LLM returns default to 'A' (task); out-of-range letters default to 'A'; lowercase valid letters are uppercased and mapped correctly; and the query is stripped before being embedded in the prompt. The
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/streaming_nlg.py generate_answer success path with a fake requests.post returning a choices payload (verify truncation threshold before asserting); Add tests for enhanced_core/correlation_checker.py edge cases beyond tests/test_correlation_checker.py

## 2026-09-19 19:52 UTC — Add tests for RejectionDetector parsing and heuristics
- **Type:** tests
- **Files:** tests/test_rejection_detector_parsing.py
- **Why:** The evolution log repeatedly lists hardening/tests for enhanced_core/rejection_detector.py, and the module is pure stdlib (logging, re) so it can be exercised with a fake llm_caller without network or heavy deps. Reading the implementation shows clear observable contracts: a bare '1'/'0' anywhere in the response is parsed via word-boundary regex, keyword fallbacks ('accept'/'reject') apply when no digit is present, and None/empty/unparseable responses default to accept (the safe default). These tests lock in that contract so future refactors cannot silently flip the default or break digit pars
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/streaming_nlg.py generate_answer success path with a fake requests.post returning a choices payload (verify truncation threshold before asserting); Add tests for enhanced_core/correlation_checker.py edge cases beyond tests/test_correlation_checker.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-19 22:00 UTC — Fix NLG prompt to use truncated data string
- **Type:** bugfix
- **Files:** enhanced_core/streaming_nlg.py
- **Why:** In enhanced_core/streaming_nlg.py generate_answer, the code computes a truncated data_str (capped at 5000 chars) and logs the truncation, but then builds nlg_prompt with json.dumps(data, indent=2, default=str) instead of data_str. The truncation is therefore dead code: oversized query results still produce an unbounded prompt, defeating the stated guard and risking oversized API requests. Using the already-computed data_str makes the truncation effective without changing the function signature or the success-path return type.
- **Next:** Add tests for enhanced_core/streaming_nlg.py generate_answer success path with a fake requests.post returning a choices payload, asserting the prompt contains the truncated data_str when data exceeds 5000 chars; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/correlation_checker.py edge cases beyond tests/test_correlation_checker.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-20 02:49 UTC — Add success-path tests for StreamingNLG.generate_answer
- **Type:** tests
- **Files:** tests/test_streaming_nlg_answer.py
- **Why:** The evolution log repeatedly lists tests for the generate_answer success path as a next idea, and the previous attempt was rejected because it asserted on the truncation threshold without verifying the implementation. Reading the current code shows the prompt is now built from the truncated data_str (capped at 5000 chars), the model is 'deepseek-chat', and failures fall back to 'Based on the data, {query}'. These tests stub 'requests' via sys.modules so no network is needed, locking in the prompt-building and fallback contract so future refactors cannot silently regress the truncation fix.
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/correlation_checker.py edge cases beyond tests/test_correlation_checker.py (e.g. whitespace-only queries); Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines

## 2026-09-20 08:57 UTC — Add tests for CorrelationChecker edge cases
- **Type:** tests
- **Files:** tests/test_correlation_checker_edge_cases.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/correlation_checker.py edge cases as a next idea. The module is pure stdlib (only logging) and takes an injected llm_caller, so it is fully testable without network or heavy deps. Reading the implementation shows clear observable contracts: empty/None prev or curr query short-circuits to False without calling the LLM, the prompt embeds both queries, empty LLM results default to False, responses starting with 'yes' (case-insensitive, after strip) are True, and anything else is False. These tests lock in that contract so future refactors
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Add tests for enhanced_core/conversation_manager.py context update/retrieval edge cases beyond tests/test_conversation_manager.py

## 2026-09-20 13:51 UTC — Add tests for RejectionDetector heuristic fallback paths
- **Type:** tests
- **Files:** tests/test_rejection_detector_heuristics.py
- **Why:** The evolution log repeatedly lists hardening/tests for enhanced_core/rejection_detector.py, and the existing tests/test_rejection_detector_parsing.py covers digit parsing and default-accept but not the keyword-heuristic branch that runs when no bare 0/1 is present. Reading the implementation shows the heuristic checks ('accept','yes','within scope') before ('reject','no','out of scope','unrelated'), so a response containing both keywords resolves to accept. These tests lock in that ordering and the safe default so future refactors cannot silently flip the contract.
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Add tests for enhanced_core/conversation_manager.py context update/retrieval edge cases beyond tests/test_conversation_manager.py; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-20 17:12 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ConversationManager context edge cases
- **Blocked by:** rejected by gate: tests/test_conversation_manager_edge_cases.py failed: ERROR: test_empty_query_returns_invalid (tests.test_conversation_manager_edge_cases.TestConversationManagerEdgeCases.test_empty_query_returns_inva
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Add tests for enhanced_core/function_registry.py registration/lookup logic in tests/test_function_registry.py (verify _execute_sql column names before asserting on company_name/executive_director_ratio)

## 2026-09-20 20:07 UTC — Add tests for RejectionDetector unparseable default-accept path
- **Type:** tests
- **Files:** tests/test_rejection_detector_defaults.py
- **Why:** The evolution log repeatedly lists hardening/tests for enhanced_core/rejection_detector.py, and the existing tests cover digit parsing and keyword heuristics but not the final fallback branch where the LLM output is unparseable (no 0/1, no keywords). Reading the implementation shows that branch logs a warning and returns True (safe default to avoid false rejections). These tests lock in that contract so a future refactor cannot silently flip the default to reject, which would break legitimate queries.
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Add tests for enhanced_core/conversation_manager.py context update/retrieval edge cases beyond tests/test_conversation_manager.py (read implementation first: prior attempt failed on empty-query expectations); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-20 23:46 UTC — Add tests for ConversationManager context and history
- **Type:** tests
- **Files:** tests/test_conversation_manager_context.py
- **Why:** The evolution log repeatedly lists ConversationManager context/history tests as a next idea, and a prior attempt failed because it asserted on empty-query behaviour without reading the implementation. Reading the code shows clear observable contracts: add_turn appends to a bounded deque, _update_context sets last_company (case-insensitive, first match wins) and always refreshes last_query/last_user_query/last_query_time, get_history_text only includes non-empty assistant lines, clear() resets context and slots, and get_stats reports counts. These tests lock in that contract with the standard l
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/function_registry.py registration/lookup logic (verify _execute_sql column names before asserting)

## 2026-09-21 02:46 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector keyword heuristic ordering
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_heuristics.py already exists
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Add tests for enhanced_core/function_registry.py registration/lookup logic (verify _execute_sql column names before asserting); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-21 09:29 UTC — Reflection: no code change landed
- **Attempted:** Add tests for FunctionRegistry dispatch and helpers
- **Blocked by:** rejected by gate: new_file 0: tests/test_function_registry.py already exists
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/parallel_executor.py timeout/error paths beyond tests/test_parallel_executor.py

## 2026-09-21 16:08 UTC — Add tests for ParallelExecutor timeout and error paths
- **Type:** tests
- **Files:** tests/test_parallel_executor_timeout.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/parallel_executor.py timeout/error paths as a next idea, and the module is pure stdlib (logging, time, concurrent.futures, dataclasses) so it is fully testable without network or heavy deps. Reading the implementation shows clear observable contracts: empty task dicts return {} without raising, non-positive max_workers or timeout raise ValueError, non-callable task values raise ValueError, a task raising an exception yields a TaskResult with error set and result None, and an overall timeout still returns a TaskResult for every submitte
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/query_rewriter.py rewrite prompt construction edge cases beyond tests/test_query_rewriter.py

## 2026-09-21 21:32 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ParallelExecutor callback error paths
- **Blocked by:** rejected by gate: tests/test_parallel_executor_callbacks.py failed: test_execution_time_recorded_on_success (tests.test_parallel_executor_callbacks.TestCallbackErrors.test_execution_time_recorded_on_success) ... ok | t
- **Next:** Document ConversationManager context keys in API_REFERENCE.md; Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/query_rewriter.py rewrite prompt construction edge cases beyond tests/test_query_rewriter.py

## 2026-09-22 00:28 UTC — Reflection: no code change landed
- **Attempted:** Remove duplicate _is_bad_rewrite in query_rewriter.py
- **Blocked by:** rejected by gate: edit 0: 'old' occurs 0 times in enhanced_core/query_rewriter.py (need exactly 1)
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/query_rewriter.py rewrite prompt construction edge cases beyond tests/test_query_rewriter.py

## 2026-09-22 07:09 UTC — Remove duplicate _is_bad_rewrite in query_rewriter.py
- **Type:** refactor
- **Files:** enhanced_core/query_rewriter.py
- **Why:** enhanced_core/query_rewriter.py defines _is_bad_rewrite twice with identical bodies (once before _build_rewrite_prompt and once after). The second definition silently shadows the first, which is dead code and confusing for maintainers; a previous attempt to fix this was rejected because the replacement text did not match verbatim. Removing the first duplicate leaves the surviving method identical in behaviour, so no caller or test is affected, and it eliminates the shadowing hazard.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/query_rewriter.py rewrite prompt construction edge cases beyond tests/test_query_rewriter.py

## 2026-09-22 12:59 UTC — Reflection: no code change landed
- **Attempted:** Add tests for QueryRewriter rewrite prompt edge cases
- **Blocked by:** rejected by gate: tests/test_query_rewriter_prompt.py failed: FAIL: test_query_is_stripped_before_embedding (tests.test_query_rewriter_prompt.TestRewritePromptConstruction.test_query_is_stripped_before_embedding) | sel
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic (verify _execute_sql column names before asserting)

## 2026-09-22 17:51 UTC — Add tests for RejectionDetector digit parsing edge cases
- **Type:** tests
- **Files:** tests/test_rejection_detector_digit_parsing.py
- **Why:** The evolution log repeatedly lists hardening/tests for enhanced_core/rejection_detector.py, and existing tests cover digit parsing, keyword heuristics, and the unparseable default. What is not locked in is the regex boundary behaviour: the \b([01])\b pattern means a bare '0'/'1' wins, but a digit embedded in a longer number (e.g. '10', '2024') must NOT be treated as a decision, and the first matching digit wins when several appear. These tests pin that contract so a future refactor of the regex cannot silently change accept/reject decisions.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic (verify _execute_sql column names before asserting)

## 2026-09-22 20:44 UTC — Reflection: no code change landed
- **Attempted:** Add tests for FinancialFunctionRegistry dispatch and helpers
- **Blocked by:** rejected by gate: new_file 0: tests/test_function_registry.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/query_rewriter.py rewrite prompt construction edge cases beyond tests/test_query_rewriter.py

## 2026-09-22 23:56 UTC — Add tests for RejectionDetector keyword heuristic ordering
- **Type:** tests
- **Files:** tests/test_rejection_detector_keyword_order.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/rejection_detector.py as a next idea, and the existing tests cover digit parsing, keyword heuristics, and the unparseable default. What is not locked in is the ordering contract of the fallback keyword scan: the accept keywords are checked before the reject keywords, so an output containing both (e.g. 'yes, but no') must resolve to Accept. These tests pin that precedence so a future refactor cannot silently flip the decision.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/query_rewriter.py rewrite prompt construction edge cases beyond tests/test_query_rewriter.py

## 2026-09-23 03:09 UTC — Add tests for QueryRewriter rewrite guard logic
- **Type:** tests
- **Files:** tests/test_query_rewriter_guard.py
- **Why:** The evolution log repeatedly lists QueryRewriter tests as a next idea, and a prior attempt failed because it asserted on prompt-construction details that did not match the implementation. Reading the code shows clear, verifiable contracts in rewrite(): empty/whitespace queries are returned stripped without calling the LLM, empty history returns the query unchanged, a falsy LLM result or a low character-overlap rewrite falls back to the original query, and a good rewrite is stripped and returned. These tests pin that behaviour without touching prompt internals.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic (verify _execute_sql column names before asserting)

## 2026-09-23 08:59 UTC — Add tests for RejectionDetector unparseable fallback paths
- **Type:** tests
- **Files:** tests/test_rejection_detector_unparseable.py
- **Why:** The evolution log repeatedly lists hardening/tests for enhanced_core/rejection_detector.py, and existing tests cover digit parsing, keyword heuristics, and keyword ordering. What is not locked in is the final safety net: when the LLM output is None, empty, or contains no digit and no keyword, should_accept must default to True (accept) and must not raise. These tests pin that contract so a future refactor of the parsing chain cannot silently flip the default or crash on None.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Document ConversationManager context keys in API_REFERENCE.md; Add tests for enhanced_core/function_registry.py registration/lookup logic (verify _execute_sql column names before asserting); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-23 14:35 UTC — Add tests for FunctionRegistry dispatch and helpers
- **Type:** tests
- **Files:** tests/test_function_registry_dispatch.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/function_registry.py as a next idea, and the module is pure stdlib (logging, json, sqlite3, typing) so it is testable without network or heavy deps. Reading the implementation shows clear observable contracts: execute() returns an error dict for unknown functions and for missing required parameters, _get_company_id returns None for empty names and no DB, and _calculate_concentration parses percentages defensively. These tests pin that behaviour so a future refactor cannot silently change the error contract.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for enhanced_core/function_registry.py _get_top_shareholders SQL construction using an in-memory sqlite3 connection

## 2026-09-23 19:22 UTC — Add tests for FunctionRegistry _execute_sql and concentration parsing
- **Type:** tests
- **Files:** tests/test_function_registry_sql.py
- **Why:** The evolution log repeatedly lists tests for enhanced_core/function_registry.py as a next idea, and the module is pure stdlib (logging, json, sqlite3, typing) so it is testable without network or heavy deps. Reading the implementation shows clear observable contracts in _execute_sql (returns [] when no backend, returns [] on sqlite3.Error, returns list of dicts keyed by column names) and in _calculate_concentration's parse_pct helper (None, '/', and non-numeric strings all map to 0.0). These tests pin that behaviour so a future refactor cannot silently change the error contract or the percenta
- **Next:** Add tests for StreamingNLG.generate_streaming input validation and stream parsing with a fake requests.post returning iter_lines; Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-23 22:36 UTC — Reflection: no code change landed
- **Attempted:** Add tests for StreamingNLG streaming input validation
- **Blocked by:** rejected by gate: tests/test_streaming_nlg_streaming.py failed: ERROR: test_empty_query_returns_error_dict (tests.test_streaming_nlg_streaming.TestGenerateStreamingValidation.test_empty_query_returns_error_dict) | Type
- **Next:** Verify StreamingNLG._parse_stream_line signature and behaviour before relying on it; add tests for the full generate_streaming happy path with a fake requests.post returning iter_lines; Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-24 02:37 UTC — Add tests for RejectionDetector llm_caller error propagation
- **Type:** tests
- **Files:** tests/test_rejection_detector_llm_errors.py
- **Why:** The evolution log repeatedly lists rejection_detector tests as a next idea, and existing tests cover digit parsing, keyword heuristics, keyword ordering, and the unparseable default. What is not locked in is the behaviour when llm_caller itself raises: should_accept currently lets the exception propagate, which callers must know about. These tests pin that contract (and the None-returning caller path) so a future refactor cannot silently swallow errors or change the accept/reject default.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-24 08:54 UTC — Add tests for RejectionDetector prompt and temperature contract
- **Type:** tests
- **Files:** tests/test_rejection_detector_prompt.py
- **Why:** The evolution log repeatedly lists rejection_detector tests as a next idea, and existing tests cover digit parsing, keyword heuristics, ordering, unparseable defaults, and llm_caller error propagation. What is not locked in is the exact prompt contract: the query must be embedded verbatim, the prompt must instruct a binary 1/0 decision, and temperature must be forwarded as 0.1. These tests pin that interface so a future prompt refactor cannot silently drop the query or change the sampling temperature.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-24 14:33 UTC — Add tests for RejectionDetector prompt edge cases
- **Type:** tests
- **Files:** tests/test_rejection_detector_prompt_edges.py
- **Why:** The evolution log repeatedly lists rejection_detector tests as a next idea, and existing tests cover digit parsing, keyword heuristics, ordering, unparseable defaults, llm_caller error propagation, and the prompt/temperature contract. What is not locked in is how the prompt handles edge-case queries: empty strings, whitespace-only input, and queries containing newlines or the literal 'Decision:' marker must still be embedded verbatim so the LLM sees the real query. These tests pin that contract so a future prompt refactor cannot silently mangle or truncate the query.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-24 19:41 UTC — Reflection: no code change landed
- **Attempted:** Add tests for FunctionRegistry registration and lookup
- **Blocked by:** rejected by gate: tests/test_function_registry_registration.py failed: ERROR: test_duplicate_registration_returns_false (tests.test_function_registry_registration.TestRegisterFunction.test_duplicate_registration_return
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-24 22:54 UTC — Add tests for RejectionDetector heuristic keyword precedence
- **Type:** tests
- **Files:** tests/test_rejection_detector_heuristic_precedence.py
- **Why:** The evolution log repeatedly lists rejection_detector tests as a next idea, and existing tests cover digit parsing, keyword heuristics, ordering, unparseable defaults, llm_caller errors, and prompt contracts. What is not locked in is the exact keyword sets and their precedence over the unparseable default: an output containing both an accept keyword and a reject keyword must resolve to Accept because accept keywords are scanned first, and an output with only a reject keyword must resolve to Reject. These tests pin that contract so a future refactor of the fallback scan cannot silently flip dec
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-25 02:54 UTC — Add tests for RejectionDetector digit parsing edge cases
- **Type:** tests
- **Files:** tests/test_rejection_detector_digit_boundaries.py
- **Why:** The evolution log repeatedly lists rejection_detector tests as a next idea, and existing tests cover keyword heuristics, ordering, unparseable defaults, llm_caller errors, and prompt contracts. What is not locked in is the digit-parsing branch itself: the regex uses word boundaries so '1' inside '10' or '2.1' must not match, while '1 (accept)', 'Decision: 0', and ' 1 ' must. These tests pin that contract so a future refactor of the regex cannot silently flip decisions on multi-digit or decimal outputs.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-25 09:15 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector digit parsing edge cases
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_digit_boundaries.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-25 14:54 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector digit parsing edge cases
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_digit_boundaries.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-25 19:45 UTC — Add tests for RejectionDetector keyword-order and digit precedence
- **Type:** tests
- **Files:** tests/test_rejection_detector_digit_keyword_precedence.py
- **Why:** The evolution log repeatedly lists rejection_detector tests as a next idea, and existing tests cover digit parsing, keyword heuristics, ordering, unparseable defaults, llm_caller errors, and prompt contracts. What is not locked in is the interaction between the digit branch and the keyword fallback: when the LLM output contains both a bare 0/1 token and contradictory keywords, the digit branch must win, and the accept-keyword scan must run before the reject-keyword scan. These tests pin that precedence so a future refactor cannot silently flip decisions.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-25 22:59 UTC — Add tests for RejectionDetector empty/None LLM output
- **Type:** tests
- **Files:** tests/test_rejection_detector_empty_output.py
- **Why:** Existing rejection_detector tests cover digit parsing, keyword heuristics, ordering, prompt contracts, and llm_caller errors, but not the boundary where the LLM returns None or an empty/whitespace-only string. In that case result_str becomes '' and the regex is skipped, so the keyword scan runs on an empty string and the safe default (accept) is returned. These tests pin that contract so a future refactor cannot accidentally reject on missing LLM output.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-26 02:58 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector unparseable-output default
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_unparseable.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-26 08:58 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector keyword-order precedence
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_keyword_order.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Guard FinancialFunctionRegistry._execute_sql against missing db and osworld backends (currently raises AttributeError; see tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend); Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise

## 2026-09-26 13:59 UTC — Reflection: no code change landed
- **Attempted:** Guard _execute_sql against missing db/osworld backends
- **Blocked by:** rejected by gate: edit 0: 'old' occurs 0 times in enhanced_core/function_registry.py (need exactly 1)
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Update tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend to assert the new empty-list contract instead of AttributeError

## 2026-09-26 17:40 UTC — Guard _execute_sql when no db/osworld backend configured
- **Type:** robustness
- **Files:** enhanced_core/function_registry.py, tests/test_function_registry_sql.py
- **Why:** FinancialFunctionRegistry._execute_sql falls through to self.db.cursor() when neither osworld nor db is configured, raising AttributeError: 'NoneType' object has no attribute 'cursor'. This is the exact issue logged as a next idea and pinned by tests/test_function_registry_sql.py::TestExecuteSqlWithoutBackend. Returning an empty list matches the module's existing error contract (SQL errors already return []), so callers that check 'if not result' keep working while the crash disappears. The existing test that asserts AttributeError is updated to the new deliberate contract.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add a test that FinancialFunctionRegistry.execute returns {'error': ...} for an unknown function name

## 2026-09-26 20:29 UTC — Add tests for FunctionRegistry unknown-function and error contract
- **Type:** tests
- **Files:** tests/test_function_registry_execute.py
- **Why:** The evolution log's next-ideas list asks for a test that FinancialFunctionRegistry.execute returns {'error': ...} for an unknown function name, and the module's error contract (unknown function, missing required parameter, backend exception) is currently untested. These tests pin the observable behaviour of execute() so a future refactor of the dispatch chain cannot silently change the return shape callers depend on.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._get_top_shareholders SQL construction (top_n interpolation) in tests/test_function_registry_sql.py

## 2026-09-27 00:05 UTC — Add tests for _get_top_shareholders SQL construction
- **Type:** tests
- **Files:** tests/test_function_registry_top_shareholders.py
- **Why:** The evolution log's next-ideas list asks for tests covering FinancialFunctionRegistry._get_top_shareholders SQL construction, especially the top_n interpolation into the LIMIT clause, which is currently untested. These tests pin the observable contract (row shape, ordering by share_percentage, top_n honoured, unknown company error) so a future refactor of the query builder cannot silently change results. They use an in-memory sqlite3 database, matching the existing test_function_registry_sql.py style, so no network or heavy deps are needed.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._calculate_concentration when top_n exceeds available rows

## 2026-09-27 07:26 UTC — Reflection: no code change landed
- **Attempted:** Add tests for _calculate_concentration edge cases
- **Blocked by:** rejected by gate: tests/test_function_registry_concentration.py failed: ERROR: test_top_n_exceeding_available_rows_is_clamped (tests.test_function_registry_concentration.TestCalculateConcentration.test_top_n_exceeding_
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-27 13:27 UTC — Reflection: no code change landed
- **Attempted:** Add tests for rejection_detector keyword heuristics
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_heuristics.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-27 18:00 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector llm_caller error propagation
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_llm_errors.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-27 22:44 UTC — Add tests for RejectionDetector prompt contract and digit boundaries
- **Type:** tests
- **Files:** tests/test_rejection_detector_prompt_contract.py
- **Why:** The evolution log repeatedly lists rejection_detector coverage as a next idea, and the existing suites cover heuristics, digit precedence, empty output and llm_caller errors, but not the prompt contract itself (scope keywords, single-query interpolation, temperature) nor the \b[01]\b boundary behaviour for multi-digit or embedded numbers. These tests pin the observable prompt/parse contract so a future refactor of the prompt template or regex cannot silently change decisions.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-28 02:59 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector keyword heuristic fallback
- **Blocked by:** rejected by gate: tests/test_rejection_detector_keyword_fallback.py failed: FAIL: test_unrecognised_text_defaults_to_accept (tests.test_rejection_detector_keyword_fallback.TestSafeDefault.test_unrecognised_text_default
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-28 10:22 UTC — Add tests for RejectionDetector keyword heuristic fallback
- **Type:** tests
- **Files:** tests/test_rejection_detector_keyword_fallback.py
- **Why:** The evolution log repeatedly lists rejection_detector coverage as a next idea, and the existing suites cover digit parsing, prompt contract, empty output and llm_caller errors, but not the keyword-heuristic branch that runs when the LLM reply contains no standalone 0/1 token. A previous attempt at this file was rejected because it wrongly assumed unrecognised text defaults to accept; reading the implementation shows the fallback checks accept-words first, then reject-words, and only then defaults to accept. These tests pin that exact precedence and the safe default so a future refactor cannot 
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-28 19:04 UTC — Add tests for RejectionDetector None/empty LLM output
- **Type:** tests
- **Files:** tests/test_rejection_detector_none_output.py
- **Why:** The evolution log's next-ideas list has repeatedly pointed at rejection_detector coverage, and the existing suites cover digit parsing, prompt contract, keyword fallback and llm_caller errors, but not the None/empty-string branch that guards str(result) before regex. That branch is the only place where a None llm_caller result is converted safely, so a future refactor could reintroduce a TypeError. These tests pin the observable contract (None and empty output fall through to the safe accept default, and llm_caller is still invoked exactly once).
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-29 00:06 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector digit-token boundary parsing
- **Blocked by:** rejected by gate: tests/test_rejection_detector_digit_token_boundaries.py failed: FAIL: test_embedded_digit_in_word_is_not_a_decision (tests.test_rejection_detector_digit_token_boundaries.TestNonStandaloneDigitsFallThr
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-29 07:44 UTC — Reflection: no code change landed
- **Attempted:** Test RejectionDetector digit-token boundary parsing
- **Blocked by:** rejected by gate: tests/test_rejection_detector_digit_token_boundaries.py failed: FAIL: test_ten_contains_standalone_zero_and_rejects (tests.test_rejection_detector_digit_token_boundaries.TestMultiDigitNumbers.test_ten
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-29 14:30 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector digit-token boundary parsing
- **Blocked by:** rejected by gate: tests/test_rejection_detector_digit_token_boundaries.py failed: FAIL: test_ten_contains_standalone_zero_and_rejects (tests.test_rejection_detector_digit_token_boundaries.TestMultiDigitNumbers.test_ten
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-29 20:22 UTC — Add tests for RejectionDetector digit-token boundary parsing
- **Type:** tests
- **Files:** tests/test_rejection_detector_digit_token_boundaries.py
- **Why:** The evolution log repeatedly lists rejection_detector digit-token boundary coverage as a next idea, and two prior attempts were rejected because they wrongly assumed \b[01]\b does not match digits embedded in multi-digit numbers. Reading the implementation confirms re.search(r'\b([01])\b', ...) matches the '0' inside '10' and the '1' inside '21', so these tests pin the real observable contract (first standalone-ish digit token wins, embedded digits in words like 'a1b' do not match) so a future refactor of the regex cannot silently change decisions.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-30 00:56 UTC — Add tests for RejectionDetector prompt construction
- **Type:** tests
- **Files:** tests/test_rejection_detector_prompt_template.py
- **Why:** The evolution log's next-ideas list repeatedly points at rejection_detector coverage, and existing suites cover digit parsing, keyword fallback, None output and llm_caller errors, but not the prompt template itself: the scope keywords, the single interpolation of the query, and the temperature passed to llm_caller. These tests pin the observable prompt contract so a future refactor of the template cannot silently drop scope rules or change the sampling temperature, and they verify the query is interpolated verbatim (including braces and newlines).
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-30 07:48 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector heuristic keyword precedence
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_heuristic_precedence.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Harden enhanced_core/rejection_detector.py: log successful parses at debug level to reduce log noise; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-09-30 14:29 UTC — Add tests for RejectionDetector unparseable-output logging
- **Type:** tests
- **Files:** tests/test_rejection_detector_unparseable_logging.py
- **Why:** The evolution log's next-ideas list keeps pointing at rejection_detector coverage, and existing suites cover digit parsing, keyword fallback, None output, prompt template and llm_caller errors, but not the final unparseable branch: when the LLM reply has no bare 0/1 token and no accept/reject keyword, should_accept logs a warning containing the raw repr and defaults to accept. That branch is the only place where the raw LLM output is surfaced for debugging, so a future refactor could silently drop the warning or change the safe default. These tests pin the observable contract (warning emitted 
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for enhanced_core/arbitrator.py tie-breaking when both agents disagree

## 2026-09-30 20:26 UTC — Add tests for arbitrator tie-breaking and LLM edge cases
- **Type:** tests
- **Files:** tests/test_arbitrator_edge_cases.py
- **Why:** The evolution log's next-ideas list points at enhanced_core/arbitrator.py coverage, and existing suites cover rejection_detector, query_rewriter, conversation_manager and function_registry but not the arbitrator's parsing contract. Reading the implementation shows arbitrate() strips/uppercases the LLM reply, defaults to 'A' (task) for None, non-string, or unrecognised letters, and short-circuits empty/whitespace queries to 'invalid' without calling the LLM. These tests pin that observable contract so a future refactor cannot silently change the safe default or the empty-query guard.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for QueryArbitrator.arbitrate when llm_caller raises an exception (check whether it propagates or is caught)

## 2026-10-01 00:59 UTC — Add tests for QueryArbitrator LLM exception propagation
- **Type:** tests
- **Files:** tests/test_arbitrator_llm_errors.py
- **Why:** The evolution log's next-ideas list explicitly asks whether QueryArbitrator.arbitrate propagates exceptions raised by llm_caller or catches them. Reading the implementation shows there is no try/except around self.llm_caller, so exceptions propagate to the caller. Existing arbitrator suites cover letter mapping, empty-query guard and fallback defaults but not this contract, so a future refactor could silently swallow errors and hide LLM failures. These tests pin the observable behaviour and also verify the empty-query guard still short-circuits before any LLM call.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for QueryArbitrator.arbitrate history interpolation with multi-line history strings

## 2026-10-01 08:07 UTC — Add tests for arbitrator history interpolation edge cases
- **Type:** tests
- **Files:** tests/test_arbitrator_history.py
- **Why:** The evolution log's next-ideas list asks for tests of QueryArbitrator.arbitrate history interpolation with multi-line history strings. Reading _build_arbitration_prompt shows history is interpolated verbatim into the 'Context:' line and the default 'No history' is used only when history is falsy, so empty string and None both fall back. Existing suites cover the default and a simple marker but not multi-line, brace-containing, or empty-string history, so a future refactor of the f-string could silently change interpolation.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for enhanced_core/query_rewriter.py when llm_caller returns None or non-string

## 2026-10-01 16:49 UTC — Reflection: no code change landed
- **Attempted:** Add tests for QueryRewriter None/non-string LLM replies
- **Blocked by:** rejected by gate: tests/test_query_rewriter_llm_replies.py failed: FAIL: test_list_reply_raises_type_error (tests.test_query_rewriter_llm_replies.TestNonStringReplyRaises.test_list_reply_raises_type_error) | with self.
- **Next:** Harden enhanced_core/query_rewriter.py: coerce non-string llm_caller replies (log a warning and return the original query) so set(rewritten) cannot raise TypeError; Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-10-01 22:12 UTC — Harden QueryRewriter against non-string LLM replies
- **Type:** robustness
- **Files:** enhanced_core/query_rewriter.py, tests/test_query_rewriter_llm_replies.py
- **Why:** rewrite() passes the llm_caller result straight into _is_bad_rewrite, which calls len(set(rewritten)) and set(rewritten).intersection(original). If a model returns a list, dict or int (a real failure mode for chat APIs), this raises TypeError and crashes the rewrite step instead of falling back to the original query. The previous run's gate rejection confirmed this failure mode. Coercing non-string replies to a safe fallback keeps the documented behaviour (return the original query when no good rewrite exists) and makes the module robust.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for enhanced_core/query_rewriter.py when the reply is a valid string but has low character overlap with the original query (bad-rewrite guard)

## 2026-10-02 03:32 UTC — Reflection: no code change landed
- **Attempted:** Add tests for QueryRewriter bad-rewrite overlap guard
- **Blocked by:** rejected by gate: tests/test_query_rewriter_bad_rewrite_guard.py failed: FAIL: test_guard_uses_distinct_chars_not_length (tests.test_query_rewriter_bad_rewrite_guard.TestBadRewriteGuard.test_guard_uses_distinct_chars_n
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for enhanced_core/query_rewriter.py when query is whitespace-only and history is present (no LLM call expected)

## 2026-10-02 10:13 UTC — Add tests for QueryRewriter whitespace-only query guard
- **Type:** tests
- **Files:** tests/test_query_rewriter_whitespace_query.py
- **Why:** The evolution log's next-ideas list asks for coverage of QueryRewriter when the query is whitespace-only and history is present, expecting no LLM call. Reading rewrite() confirms the first guard returns query.strip() (empty string) before any history check or llm_caller invocation, and that a None query is returned as-is. Existing suites cover non-string replies, good rewrites and the no-history short circuit but not this guard, so a future refactor could silently start calling the LLM on empty input.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for enhanced_core/query_rewriter.py bad-rewrite overlap guard using distinct-character counts (overlap < len(original)/4) rather than length

## 2026-10-02 17:13 UTC — Add tests for QueryRewriter bad-rewrite overlap guard
- **Type:** tests
- **Files:** tests/test_query_rewriter_bad_rewrite_guard.py
- **Why:** The evolution log's next-ideas list asks for coverage of the bad-rewrite overlap guard using distinct-character counts (overlap < len(original)/4). Reading _is_bad_rewrite confirms it compares len(set(rewritten).intersection(original)) against len(original)/4, so a rewrite sharing fewer than a quarter of the original's distinct characters is rejected and the original query returned. Existing suites cover non-string replies, whitespace guards and good rewrites but not this guard, so a future refactor could silently weaken it.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for enhanced_core/conversation_manager.py history trimming when it exceeds max length

## 2026-10-02 21:41 UTC — Add tests for ConversationManager history trimming
- **Type:** tests
- **Files:** tests/test_conversation_manager_history_trim.py
- **Why:** The evolution log's next-ideas list asks for coverage of conversation_manager history trimming when it exceeds max length. Reading the implementation shows history is a deque(maxlen=max_history), so appending beyond the cap silently drops the oldest turn while context keeps updating from the newest turn; get_history_text also slices the last n_turns. No existing suite pins this trimming contract, so a future refactor to a plain list could silently grow memory or change get_history_text output.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.get_history_text when a turn has an empty assistant answer (assistant line omitted)

## 2026-10-03 00:51 UTC — Reflection: no code change landed
- **Attempted:** Add tests for get_history_text empty-assistant handling
- **Blocked by:** rejected by gate: tests/test_conversation_manager_history_text.py failed: FAIL: test_n_turns_zero_returns_empty_string (tests.test_conversation_manager_history_text.TestGetHistoryText.test_n_turns_zero_returns_empty_st
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.get_context_summary when only entities are set (no last_company)

## 2026-10-03 07:25 UTC — Add tests for ConversationManager.get_context_summary
- **Type:** tests
- **Files:** tests/test_conversation_manager_context_summary.py
- **Why:** The evolution log's next-ideas list asks for coverage of get_context_summary when only entities are set (no last_company). Reading the implementation shows it joins 'Last company' and 'Entities' with '; ' and returns the literal 'No context' when both are empty; clear() resets both. No existing suite pins this output format, so a future refactor could silently change the summary string that feeds prompts.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.get_history_text when a turn has an empty assistant answer (assistant line omitted)

## 2026-10-03 12:55 UTC — Reflection: no code change landed
- **Attempted:** Add tests for get_history_text empty-assistant handling
- **Blocked by:** rejected by gate: tests/test_conversation_manager_history_text.py failed: FAIL: test_n_turns_zero_returns_empty_string (tests.test_conversation_manager_history_text.TestGetHistoryText.test_n_turns_zero_returns_empty_st
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn entity extraction when the query contains no known company name

## 2026-10-03 17:42 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ConversationManager.get_history_text
- **Blocked by:** rejected by gate: tests/test_conversation_manager_history_text.py failed: FAIL: test_n_turns_zero_returns_empty_string (tests.test_conversation_manager_history_text.TestGetHistoryText.test_n_turns_zero_returns_empty_st
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn entity extraction when the query contains no known company name

## 2026-10-03 20:26 UTC — Add tests for ConversationManager.get_history_text
- **Type:** tests
- **Files:** tests/test_conversation_manager_history_text.py
- **Why:** The evolution log repeatedly lists get_history_text coverage as a next idea; two prior attempts were rejected because they asserted an n_turns=0 behaviour that does not match the implementation. Reading the code shows list(self.history)[-n_turns:] with n_turns=0 yields the full history (not an empty string), and the assistant line is omitted only when turn.assistant is falsy. These tests pin the real contract, including the empty-assistant and n_turns=0 cases, so a future refactor cannot silently change the prompt history format.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn entity extraction when the query contains no known company name

## 2026-10-04 00:17 UTC — Add tests for ConversationManager.add_turn entity extraction
- **Type:** tests
- **Files:** tests/test_conversation_manager_entity_extraction.py
- **Why:** The evolution log repeatedly lists add_turn entity extraction as a next idea. Reading conversation_manager.py shows add_turn extracts known company names from the query into self.context['entities'] and sets last_company, while queries with no known company leave entities untouched. No existing suite pins this contract, so a refactor of the extraction regex or the known-company list could silently break context tracking that feeds prompts.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn when the query contains multiple known companies (order of entities)

## 2026-10-04 07:38 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ConversationManager multi-company entity order
- **Blocked by:** rejected by gate: tests/test_conversation_manager_multi_entity.py failed: ERROR: test_reversed_query_order_is_respected (tests.test_conversation_manager_multi_entity.TestMultiEntityExtraction.test_reversed_query_order_
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn when the query contains a known company name as a substring of a longer word (word-boundary behaviour)

## 2026-10-04 13:36 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ConversationManager multi-company entity order
- **Blocked by:** rejected by gate: tests/test_conversation_manager_multi_entity.py failed: FAIL: test_two_companies_in_query_are_both_recorded (tests.test_conversation_manager_multi_entity.TestMultiEntityExtraction.test_two_companies_i
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn when a known company name appears as a substring of a longer word (word-boundary behaviour)

## 2026-10-04 17:56 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ConversationManager entity word-boundary behaviour
- **Blocked by:** rejected by gate: tests/test_conversation_manager_entity_boundary.py:33: expected ':' (change would break syntax)
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn when the query contains multiple known companies (verify actual order semantics before asserting)

## 2026-10-04 20:49 UTC — Add tests for ConversationManager multi-company entity order
- **Type:** tests
- **Files:** tests/test_conversation_manager_multi_entity.py
- **Why:** The evolution log repeatedly lists multi-company entity extraction as a next idea, and two prior attempts were rejected by the gate because they asserted an order that does not match the implementation. Reading _update_context shows the loop over the fixed companies list breaks after the first match, so only the first company in the list order (not the query order) is recorded and entities never holds more than one entry per turn. These tests pin that real contract so a future refactor of the extraction loop cannot silently change context tracking that feeds prompts.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn when a known company name appears as a substring of a longer word (word-boundary behaviour)

## 2026-10-05 00:21 UTC — Reflection: no code change landed
- **Attempted:** Add tests for RejectionDetector prompt template contract
- **Blocked by:** rejected by gate: new_file 0: tests/test_rejection_detector_prompt_contract.py already exists
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for ConversationManager.add_turn when a known company name appears as a substring of a longer word (word-boundary behaviour)

## 2026-10-05 08:04 UTC — Reflection: no code change landed
- **Attempted:** Add tests for ConversationManager word-boundary entity matching
- **Blocked by:** rejected by gate: tests/test_conversation_manager_entity_boundary.py failed: FAIL: test_boundary_match_is_case_insensitive (tests.test_conversation_manager_entity_boundary.TestEntityBoundary.test_boundary_match_is_case
- **Next:** Verify the exact regex in conversation_manager._update_context before adding more boundary tests; Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines; Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown

## 2026-10-05 18:59 UTC — Add tests for run.py menu choice validation
- **Type:** tests
- **Files:** tests/test_run_menu.py
- **Why:** run.py's interactive menu validation (non-digit input, out-of-range digits, empty input defaulting to 0, and the isatty fallback) is pure logic that no existing suite covers; a refactor of the guard could silently break the CLI entry point. The tests stub stdin/stdout and patch the run_* handlers so no demo or network code is executed.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py print_menu banner/menu text so the CLI contract is pinned

## 2026-10-06 01:03 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py banner and menu text
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_has_rocket_border_lines (tests.test_run_banner_menu.TestPrintBanner.test_banner_has_rocket_border_lines) | self.assertEqual(lines[0], '\U0001f68
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py run_demo/run_test/run_main lazy imports (patch builtins.__import__ or sys.modules to assert the right module is imported)

## 2026-10-06 08:25 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py banner and menu text
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_contains_title_lines (tests.test_run_banner_menu.TestPrintBanner.test_banner_contains_title_lines) | self.assertIn('FinTalk.AI - Enhanced Financ
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py run_demo/run_test/run_main lazy imports (patch sys.modules to assert the right module is imported)

## 2026-10-06 16:25 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py banner and menu text
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_has_four_lines (tests.test_run_banner_menu.TestPrintBanner.test_banner_has_four_lines) | self.assertEqual(len(text.splitlines()), 4) | Assertion
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py run_demo/run_test/run_main lazy imports (patch sys.modules to assert the right module is imported)

## 2026-10-06 22:07 UTC — Add tests for run.py lazy imports in run_demo/run_test/run_main
- **Type:** tests
- **Files:** tests/test_run_lazy_imports.py
- **Why:** The evolution log repeatedly lists run.py lazy-import coverage as a next idea, and the earlier banner/menu-text attempts were rejected because they asserted exact banner strings that do not match the implementation. The lazy imports are pure control flow: each handler imports a specific module and calls a specific entry point. Patching sys.modules with stub modules lets us pin those module paths and call targets without executing any demo, network or heavy-dependency code.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.main menu dispatch: patch run_demo/run_test/run_main and feed choices 1/2/3/0 via patched stdin to pin the loop's break behaviour

## 2026-10-07 03:43 UTC — Add tests for run.main menu dispatch and loop exit
- **Type:** tests
- **Files:** tests/test_run_menu_dispatch.py
- **Why:** The evolution log repeatedly lists run.main menu dispatch as a next idea. main() is pure control flow: it validates the choice, dispatches to run_demo/run_test/run_main, and breaks out of the loop. No existing suite pins this behaviour, so a refactor of the guard or the break statements could silently break the CLI entry point. The tests patch the handlers and feed input via a patched stdin so no demo or network code runs.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.main non-tty fallback: patch sys.stdin.isatty to False and assert the loop exits immediately

## 2026-10-07 10:45 UTC — Add tests for run.main non-tty fallback exit
- **Type:** tests
- **Files:** tests/test_run_non_tty.py
- **Why:** The evolution log lists run.main non-tty fallback as the next idea: when sys.stdin.isatty() is False, main() must default the choice to '0' and exit immediately without dispatching any handler. This is the guard that keeps the CLI from hanging in piped/CI environments, and no existing suite pins it. The tests patch sys.stdin with a non-tty StringIO and assert no handler runs and the loop terminates.
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.main KeyboardInterrupt handling in the __main__ guard (patch run.main to raise KeyboardInterrupt)

## 2026-10-07 18:15 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py __main__ KeyboardInterrupt and error guard
- **Blocked by:** rejected by gate: tests/test_run_main_guard.py failed: FAIL: test_generic_exception_exits_with_code_one (tests.test_run_main_guard.TestMainGuard.test_generic_exception_exits_with_code_one) | self.assertEqual(code, 1) |
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py print_banner/print_menu output shape (count lines, assert key substrings) now that dispatch and guard are pinned

## 2026-10-07 23:57 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py print_banner/print_menu output shape
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_border_lines_are_rockets (tests.test_run_banner_menu.TestPrintBanner.test_banner_border_lines_are_rockets) | self.assertEqual(lines[0], '\U0001f
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py __main__ guard: patch run.main to raise KeyboardInterrupt and assert no sys.exit, then raise a generic Exception and assert sys.exit(1) is called

## 2026-10-08 04:50 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py __main__ guard error handling
- **Blocked by:** rejected by gate: tests/test_run_main_guard.py failed: FAIL: test_generic_exception_exits_with_code_one (tests.test_run_main_guard.TestMainGuard.test_generic_exception_exits_with_code_one) | exit_mock.assert_called_onc
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py print_banner/print_menu output shape by reading the exact strings from run.py before asserting

## 2026-10-08 12:36 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py banner and menu output shape
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_border_lines_are_rockets (tests.test_run_banner_menu.TestPrintBanner.test_banner_border_lines_are_rockets) | self.assertEqual(lines[0], '\U0001f
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py __main__ guard: patch run.main to raise KeyboardInterrupt and assert no sys.exit, then raise a generic Exception and assert sys.exit(1) is called

## 2026-10-08 19:36 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py banner and menu output shape
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_border_lines_are_rockets (tests.test_run_banner_menu.TestPrintBanner.test_banner_border_lines_are_rockets) | self.assertEqual(lines[0], '\U0001f
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py __main__ guard: patch run.main to raise KeyboardInterrupt and assert no sys.exit, then raise a generic Exception and assert sys.exit(1) is called

## 2026-10-09 00:05 UTC — Reflection: no code change landed
- **Attempted:** Add tests for run.py print_banner/print_menu exact output
- **Blocked by:** rejected by gate: tests/test_run_banner_menu.py failed: FAIL: test_banner_border_lines_are_rockets (tests.test_run_banner_menu.TestPrintBanner.test_banner_border_lines_are_rockets) | self.assertEqual(lines[3], '\U0001f
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py __main__ guard: patch run.main to raise KeyboardInterrupt and assert no sys.exit, then raise a generic Exception and assert sys.exit(1) is called

## 2026-10-09 08:17 UTC — Reflection: no code change landed
- **Attempted:** Add tests for QueryRewriter.rewrite non-string and bad-rewrite guards
- **Blocked by:** rejected by gate: tests/test_query_rewriter_rewrite_guards.py failed: ERROR: test_query_rewriter_rewrite_guards (unittest.loader._FailedTest.test_query_rewriter_rewrite_guards) | ImportError: Failed to import test modu
- **Next:** Add tests for StreamingNLG.generate_streaming input validation using a fake requests.post returning iter_lines (verify _parse_stream_line signature first); Document ConversationManager context keys in API_REFERENCE.md; Add tests for FinancialFunctionRegistry._compare_companies when one company is unknown; Add tests for run.py __main__ guard: patch run.main to raise KeyboardInterrupt and assert no sys.exit, then raise a generic Exception and assert sys.exit(1) is called

