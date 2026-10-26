/**
 * CH-07: deterministic, engine-independent input/privacy-contract oracle.
 * Run: node worklines/chaos/CH07_STATIC_ORACLE.mjs
 * This does not test the authoritative engine or any room/client projection.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const A = JSON.parse(readFileSync(join(dir, 'CH06_H11_A_PREDEATH_WITNESS.json'), 'utf8'));
const B = JSON.parse(readFileSync(join(dir, 'CH05_H11_H15_EARLY_DEATH_WITNESS.json'), 'utf8'));
const results = [];
function expect(id, test) {
  assert.ok(test, 'CH07 STATIC FAILURE: ' + id);
  results.push({ id, result: 'PASS_STATIC_REFERENCE' });
}
function recruit(candidates, seed) {
  const rand = (Math.imul(seed >>> 0, 1664525) + 1013904223) >>> 0;
  return candidates[rand % candidates.length];
}
function authorityReference(candidates, seed, killed) {
  const recruitedId = recruit(candidates, seed);
  const failed = recruitedId === killed;
  return { recruitedId, lifecycle: failed ? 'FAILED' : 'ACTIVE', used: true,
    activeBinding: failed ? null : recruitedId };
}
function lawfulCaptureDisplay(fixture) {
  // Capture and genuine reveal are ordinarily public. This is NOT an engine view.
  const capture = fixture.capture;
  return { event: 'ordinary_capture', moving_piece: fixture.attacker,
    destination: fixture.destination,
    captured_piece: capture.id, captured_original_color: capture.real.color,
    captured_original_type: capture.real.type,
    selected_training_type: 'cannon', training_opportunity_used: true,
    shared_training_start_event: true };
}
function publicReference(fixture, _secretState) {
  // Legitimately different private bindings must not create training-specific leaks.
  return lawfulCaptureDisplay(fixture);
}
const privateFields = ['pieceId', 'trainingPieceId', 'progress', 'failed',
  'graduated', 'activeBinding', 'trainingStatus', 'remainingTurns', 'secretRecruitSeed'];
function forbiddenPublicTrainingInfo(view) {
  // Applied to training-origin public fields, NOT ordinary captured-piece IDs.
  return privateFields.filter(k => Object.hasOwn(view, k));
}
function afterShuffleReference(secretState) {
  if (secretState.lifecycle === 'FAILED') return {
    ...secretState, lifecycle: 'FAILED', activeBinding: null, used: true };
  return secretState; // Active rebind remains main-owned, not tested here.
}
const fixtures = [
  { code: 'A', source: A, openingSeed: A.opening.seed,
    candidates: A.H15.candidates_ordered, deadSeed: 0, liveSeed: 1,
    capture: { id: A.moves[0].target.id, real: A.moves[0].target.original_true_identity },
    attacker: A.moves[0].piece_id, destination: A.moves[0].to,
    expectedDead: 'covered-25', expectedLive: 'covered-00' },
  { code: 'B', source: B, openingSeed: B.algorithm.opening_seed,
    candidates: B.training.original_red_cannon_candidate_ids, deadSeed: 1, liveSeed: 0,
    capture: { id: B.moves[2].captured.id, real: B.moves[2].captured.original_true_identity },
    attacker: B.moves[2].id, destination: B.moves[2].to,
    expectedDead: 'covered-08', expectedLive: 'covered-13' },
];
for (const f of fixtures) {
  const p = f.code, dead = authorityReference(f.candidates, f.deadSeed, f.capture.id);
  const live = authorityReference(f.candidates, f.liveSeed, f.capture.id);
  expect(p + '01_SEED_AND_TYPE', f.openingSeed === (p === 'A' ? 476 : 92) &&
    f.capture.real.color === 'red' && f.capture.real.type === 'cannon');
  expect(p + '02_RECRUITMENT_PAIR', dead.recruitedId === f.expectedDead &&
    live.recruitedId === f.expectedLive && f.expectedDead !== f.expectedLive);
  expect(p + '03_PRIVATE_OUTCOME_CONTRAST', dead.lifecycle === 'FAILED' &&
    live.lifecycle === 'ACTIVE' && dead.activeBinding === null &&
    live.activeBinding === live.recruitedId && dead.used && live.used);
  const publiclyDead = publicReference(f, dead), publiclyLive = publicReference(f, live);
  expect(p + '04_SAME_ORDINARY_PUBLIC_EVENT',
    JSON.stringify(publiclyDead) === JSON.stringify(publiclyLive) &&
    publiclyDead.captured_piece === f.expectedDead);
  expect(p + '05_REVEAL_IS_LEGAL_PUBLIC_EVENT',
    publiclyDead.captured_original_type === 'cannon' &&
    publiclyDead.captured_original_color === 'red');
  expect(p + '06_NO_TRAINING_PRIVATE_FIELDS',
    forbiddenPublicTrainingInfo(publiclyDead).length === 0 &&
    forbiddenPublicTrainingInfo(publiclyLive).length === 0);
  const injected = { ...publiclyDead, pieceId: dead.recruitedId,
    progress: 1, failed: true };
  expect(p + '07_FORBIDDEN_INJECTION_IS_REJECTED',
    ['pieceId', 'progress', 'failed'].every(key =>
      forbiddenPublicTrainingInfo(injected).includes(key)));
  const restored = afterShuffleReference(dead);
  expect(p + '08_FAILED_CHANCE_STAYS_SPENT_REFERENCE',
    restored.lifecycle === 'FAILED' && restored.used &&
    restored.activeBinding === null && restored.recruitedId === dead.recruitedId);
}
expect('X01_SOURCE_FIXTURES_UNRUN',
  A.hard_gates.engine_runs === 0 && B.checks.engine_runs === 0);
expect('X02_NO_H11_H06_THIRD_HERO',
  A.hero_pair.red.includes('sky_admiral') && A.hero_pair.black.includes('shuffler') &&
  B.heroes.red.includes('sky_admiral') && B.heroes.black.includes('shuffler'));
console.log(JSON.stringify({ tool: 'CH07_STATIC_ORACLE', status: 'PASS_STATIC_REFERENCE',
  checks: results.length, engine_runs: 0, actual_room_projection_checks: 0,
  authoritative_legal_prefixes: 0, results }, null, 2));
