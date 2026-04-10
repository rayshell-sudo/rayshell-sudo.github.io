---
layout: default
title: Dot Democracy
---

# Dot Democracy MVP

Use five dots to vote on the ideas below. Enter a name to identify your votes on this device.

Admins can edit proposal titles at the bottom of this page without changing code.

<section id="dot-democracy" aria-label="Dot democracy voting board">
    <form id="user-form" novalidate>
        <label for="user-name">Your name</label>
        <div class="user-row">
            <input id="user-name" name="userName" type="text" maxlength="40" placeholder="e.g. Taylor" required>
            <button type="submit">Start Voting</button>
        </div>
        <p id="user-message" role="status" aria-live="polite"></p>
    </form>

    <div id="voting-app" hidden>
        <div class="status-panel" aria-live="polite">
            <p id="active-user"></p>
            <p id="remaining-votes"></p>
        </div>
        <ul id="proposal-list"></ul>
    </div>

    <details id="admin-panel">
        <summary>Admin Proposal Editor</summary>
        <p class="admin-note">Changes are stored in this browser only. They do not sync across devices.</p>

        <form id="admin-form" novalidate>
            <ul id="admin-proposal-list" aria-live="polite"></ul>

            <div class="admin-actions">
                <button type="button" id="add-proposal-btn">Add Proposal</button>
                <button type="submit" id="save-proposals-btn">Save Proposals</button>
                <button type="button" id="reset-proposals-btn">Reset Defaults</button>
            </div>

            <p id="admin-message" role="status" aria-live="polite"></p>
        </form>
    </details>
</section>

<style>
    #dot-democracy {
        margin-top: 1.5rem;
        padding: 1.25rem;
        border: 1px solid #d7e2eb;
        border-radius: 10px;
        background: #f8fbfe;
    }

    #user-form {
        display: grid;
        gap: 0.5rem;
    }

    #user-form label {
        font-size: 0.95rem;
        font-weight: 600;
    }

    .user-row {
        display: grid;
        grid-template-columns: minmax(180px, 320px) auto;
        gap: 0.5rem;
        align-items: center;
    }

    #user-name {
        border: 1px solid #c3cfda;
        border-radius: 6px;
        padding: 0.5rem 0.65rem;
        font-size: 1rem;
    }

    #user-form button,
    .proposal-controls button,
    .admin-actions button,
    .admin-proposal-row button {
        border: 0;
        border-radius: 6px;
        padding: 0.55rem 0.85rem;
        cursor: pointer;
        font-weight: 600;
    }

    #user-message {
        min-height: 1.2rem;
        margin: 0;
        color: #b21f2d;
        font-size: 0.9rem;
    }

    .status-panel {
        margin-top: 1rem;
        padding: 0.8rem;
        border-radius: 8px;
        background: #fff;
        border: 1px solid #d7e2eb;
    }

    .status-panel p {
        margin: 0.15rem 0;
    }

    #proposal-list {
        list-style: none;
        margin: 1rem 0 0;
        padding: 0;
        display: grid;
        gap: 0.75rem;
    }

    .proposal-card {
        background: #fff;
        border: 1px solid #d7e2eb;
        border-radius: 8px;
        padding: 0.8rem;
        display: grid;
        grid-template-columns: minmax(180px, 1fr) auto;
        gap: 0.75rem;
        align-items: center;
    }

    .proposal-title {
        margin: 0;
        font-weight: 600;
    }

    .proposal-totals {
        margin: 0.35rem 0 0;
        color: #39566f;
        font-size: 0.95rem;
    }

    .proposal-controls {
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    .proposal-controls button {
        width: 2.1rem;
        height: 2.1rem;
        padding: 0;
        font-size: 1.2rem;
        line-height: 1;
    }

    .proposal-controls .vote-count {
        min-width: 1.8rem;
        text-align: center;
        font-weight: 700;
    }

    #admin-panel {
        margin-top: 1rem;
        border: 1px solid #d7e2eb;
        border-radius: 8px;
        background: #fff;
        padding: 0.8rem;
    }

    #admin-panel summary {
        cursor: pointer;
        font-weight: 700;
    }

    .admin-note {
        margin: 0.75rem 0;
        color: #39566f;
        font-size: 0.92rem;
    }

    #admin-proposal-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: grid;
        gap: 0.5rem;
    }

    .admin-proposal-row {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 0.5rem;
        align-items: center;
    }

    .admin-proposal-row input {
        border: 1px solid #c3cfda;
        border-radius: 6px;
        padding: 0.45rem 0.6rem;
        font-size: 1rem;
    }

    .admin-proposal-row button {
        background: #f0f4f8;
        color: #243647;
    }

    .admin-actions {
        margin-top: 0.8rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    #admin-message {
        min-height: 1.2rem;
        margin: 0.6rem 0 0;
        color: #39566f;
        font-size: 0.9rem;
    }

    @media (max-width: 680px) {
        .user-row {
            grid-template-columns: 1fr;
        }

        #user-form button {
            width: 100%;
        }

        .proposal-card {
            grid-template-columns: 1fr;
            align-items: start;
        }

        .proposal-controls {
            justify-content: start;
        }

        .admin-proposal-row {
            grid-template-columns: 1fr;
        }

        .admin-actions button {
            width: 100%;
        }
    }
</style>

<script>
    (() => {
        const MAX_VOTES_PER_USER = 5;
        const STORAGE_KEY = 'dot-democracy-mvp-v1';
        const defaultProposals = [
            { id: 'support-hours', title: 'Extend support hours' },
            { id: 'feature-requests', title: 'Public feature request board' },
            { id: 'docs-refresh', title: 'Refresh site documentation' },
            { id: 'mobile-layout', title: 'Improve mobile layout' },
            { id: 'community-events', title: 'Run monthly community events' }
        ];

        const userForm = document.getElementById('user-form');
        const userNameInput = document.getElementById('user-name');
        const userMessage = document.getElementById('user-message');
        const votingApp = document.getElementById('voting-app');
        const activeUser = document.getElementById('active-user');
        const remainingVotes = document.getElementById('remaining-votes');
        const proposalList = document.getElementById('proposal-list');
        const adminForm = document.getElementById('admin-form');
        const adminProposalList = document.getElementById('admin-proposal-list');
        const addProposalButton = document.getElementById('add-proposal-btn');
        const resetProposalsButton = document.getElementById('reset-proposals-btn');
        const adminMessage = document.getElementById('admin-message');

        const sanitizeName = (name) => name.trim().toLowerCase();
        const displayName = (name) => name.trim();
        const deepClone = (value) => JSON.parse(JSON.stringify(value));

        const makeSlug = (title) => {
            const slug = title
                .trim()
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/^-+|-+$/g, '');

            return slug || 'proposal';
        };

        const normalizeProposals = (proposalListInput) => {
            const source = Array.isArray(proposalListInput) ? proposalListInput : [];
            const candidateProposals = source.length ? source : deepClone(defaultProposals);
            const seenIds = new Set();
            const normalized = [];

            candidateProposals.forEach((proposal, index) => {
                const rawTitle = typeof proposal.title === 'string' ? proposal.title.trim() : '';

                if (!rawTitle) {
                    return;
                }

                const baseId = typeof proposal.id === 'string' && proposal.id.trim()
                    ? makeSlug(proposal.id)
                    : makeSlug(rawTitle);

                let uniqueId = baseId;
                let suffix = 2;
                while (seenIds.has(uniqueId)) {
                    uniqueId = `${baseId}-${suffix}`;
                    suffix += 1;
                }

                seenIds.add(uniqueId);
                normalized.push({ id: uniqueId, title: rawTitle });
            });

            if (!normalized.length) {
                return deepClone(defaultProposals);
            }

            return normalized;
        };

        const defaultState = {
            users: {},
            proposals: deepClone(defaultProposals)
        };

        const isPlainObject = (value) => Boolean(value) && typeof value === 'object' && !Array.isArray(value);

        const pruneUserVotes = (state) => {
            const proposalIds = new Set(state.proposals.map((proposal) => proposal.id));

            Object.keys(state.users).forEach((userKey) => {
                if (!isPlainObject(state.users[userKey])) {
                    state.users[userKey] = {};
                    return;
                }

                Object.keys(state.users[userKey]).forEach((proposalId) => {
                    if (!proposalIds.has(proposalId)) {
                        delete state.users[userKey][proposalId];
                        return;
                    }

                    const value = state.users[userKey][proposalId];
                    state.users[userKey][proposalId] = Number.isInteger(value) && value >= 0 ? value : 0;
                });

                state.proposals.forEach((proposal) => {
                    if (!Number.isInteger(state.users[userKey][proposal.id])) {
                        state.users[userKey][proposal.id] = 0;
                    }
                });
            });
        };

        const normalizeState = (stateInput) => {
            const state = {
                users: isPlainObject(stateInput && stateInput.users) ? stateInput.users : {},
                proposals: normalizeProposals(stateInput && stateInput.proposals)
            };

            pruneUserVotes(state);
            return state;
        };

        const getState = () => {
            try {
                const raw = localStorage.getItem(STORAGE_KEY);
                if (!raw) {
                    return deepClone(defaultState);
                }

                const parsed = JSON.parse(raw);
                return normalizeState(parsed);
            } catch {
                return deepClone(defaultState);
            }
        };

        const saveState = (state) => {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(normalizeState(state)));
        };

        const ensureUserVotes = (state, userKey) => {
            if (!state.users[userKey]) {
                state.users[userKey] = {};
            }

            state.proposals.forEach((proposal) => {
                if (!Number.isInteger(state.users[userKey][proposal.id])) {
                    state.users[userKey][proposal.id] = 0;
                }
            });
        };

        const totalVotesByUser = (state, userKey) => {
            ensureUserVotes(state, userKey);
            return state.proposals.reduce((sum, proposal) => sum + state.users[userKey][proposal.id], 0);
        };

        const totalVotesByProposal = (state, proposalId) => {
            return Object.values(state.users).reduce((sum, userVotes) => {
                const votes = Number.isInteger(userVotes[proposalId]) ? userVotes[proposalId] : 0;
                return sum + votes;
            }, 0);
        };

        let currentUserKey = '';
        let currentUserLabel = '';

        const renderStatus = (state) => {
            const usedVotes = totalVotesByUser(state, currentUserKey);
            const availableVotes = MAX_VOTES_PER_USER - usedVotes;
            activeUser.textContent = `Voting as: ${currentUserLabel}`;
            remainingVotes.textContent = `Votes remaining: ${availableVotes} of ${MAX_VOTES_PER_USER}`;
        };

        const changeVote = (proposalId, delta) => {
            const state = getState();
            ensureUserVotes(state, currentUserKey);

            const currentValue = state.users[currentUserKey][proposalId];
            const usedVotes = totalVotesByUser(state, currentUserKey);

            if (delta > 0 && usedVotes >= MAX_VOTES_PER_USER) {
                userMessage.textContent = `You have already used all ${MAX_VOTES_PER_USER} votes.`;
                return;
            }

            if (delta < 0 && currentValue <= 0) {
                return;
            }

            state.users[currentUserKey][proposalId] = currentValue + delta;
            saveState(state);
            userMessage.textContent = '';
            render(state);
        };

        const proposalCard = (state, proposal) => {
            const userVotes = state.users[currentUserKey][proposal.id];
            const totalVotes = totalVotesByProposal(state, proposal.id);

            const card = document.createElement('li');
            card.className = 'proposal-card';

            const content = document.createElement('div');
            const title = document.createElement('p');
            title.className = 'proposal-title';
            title.textContent = proposal.title;

            const totals = document.createElement('p');
            totals.className = 'proposal-totals';
            totals.textContent = `Total votes: ${totalVotes}`;

            content.appendChild(title);
            content.appendChild(totals);

            const controls = document.createElement('div');
            controls.className = 'proposal-controls';

            const removeButton = document.createElement('button');
            removeButton.type = 'button';
            removeButton.setAttribute('aria-label', `Remove vote from ${proposal.title}`);
            removeButton.textContent = '−';
            removeButton.addEventListener('click', () => changeVote(proposal.id, -1));

            const count = document.createElement('span');
            count.className = 'vote-count';
            count.textContent = String(userVotes);

            const addButton = document.createElement('button');
            addButton.type = 'button';
            addButton.setAttribute('aria-label', `Add vote to ${proposal.title}`);
            addButton.textContent = '+';
            addButton.addEventListener('click', () => changeVote(proposal.id, 1));

            controls.appendChild(removeButton);
            controls.appendChild(count);
            controls.appendChild(addButton);

            card.appendChild(content);
            card.appendChild(controls);

            return card;
        };

        const render = (state) => {
            ensureUserVotes(state, currentUserKey);
            renderStatus(state);

            proposalList.innerHTML = '';
            state.proposals.forEach((proposal) => {
                proposalList.appendChild(proposalCard(state, proposal));
            });
        };

        const adminProposalRow = (proposal) => {
            const item = document.createElement('li');
            item.className = 'admin-proposal-row';

            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.maxLength = 120;
            titleInput.placeholder = 'Proposal title';
            titleInput.value = proposal.title;
            titleInput.dataset.proposalId = proposal.id;

            const removeButton = document.createElement('button');
            removeButton.type = 'button';
            removeButton.textContent = 'Remove';
            removeButton.addEventListener('click', () => {
                item.remove();
                adminMessage.textContent = '';
            });

            item.appendChild(titleInput);
            item.appendChild(removeButton);

            return item;
        };

        const renderAdminProposals = (state) => {
            adminProposalList.innerHTML = '';
            state.proposals.forEach((proposal) => {
                adminProposalList.appendChild(adminProposalRow(proposal));
            });
        };

        const saveProposalsFromAdmin = () => {
            const rows = Array.from(adminProposalList.querySelectorAll('.admin-proposal-row input'));
            const draftProposals = rows
                .map((input) => ({
                    id: input.dataset.proposalId || '',
                    title: input.value.trim()
                }))
                .filter((proposal) => proposal.title.length > 0);

            if (!draftProposals.length) {
                adminMessage.textContent = 'Add at least one proposal before saving.';
                return;
            }

            const state = getState();
            state.proposals = normalizeProposals(draftProposals);
            pruneUserVotes(state);
            saveState(state);
            renderAdminProposals(state);
            adminMessage.textContent = 'Proposal list saved.';

            if (currentUserKey) {
                render(state);
            }
        };

        const resetDefaultProposals = () => {
            const state = getState();
            state.proposals = deepClone(defaultProposals);
            pruneUserVotes(state);
            saveState(state);
            renderAdminProposals(state);
            adminMessage.textContent = 'Proposal list reset to defaults.';

            if (currentUserKey) {
                render(state);
            }
        };

        userForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const entered = displayName(userNameInput.value);
            const userKey = sanitizeName(entered);

            if (!userKey) {
                userMessage.textContent = 'Enter your name to begin voting.';
                return;
            }

            const state = getState();
            ensureUserVotes(state, userKey);
            saveState(state);

            currentUserKey = userKey;
            currentUserLabel = entered;
            votingApp.hidden = false;
            userMessage.textContent = '';
            render(state);
        });

        adminForm.addEventListener('submit', (event) => {
            event.preventDefault();
            saveProposalsFromAdmin();
        });

        addProposalButton.addEventListener('click', () => {
            adminProposalList.appendChild(adminProposalRow({ id: '', title: '' }));
            adminMessage.textContent = '';
        });

        resetProposalsButton.addEventListener('click', () => {
            resetDefaultProposals();
        });

        const initialState = getState();
        saveState(initialState);
        renderAdminProposals(initialState);
    })();
</script>
