---
layout: default
title: Dot Democracy
---

# Dot Democracy MVP

Use five dots to vote on the ideas below. Enter a name to identify your votes on this device.

<section id="dot-democracy" aria-label="Dot democracy voting board">
    <form id="voter-form" novalidate>
        <label for="voter-name">Your name</label>
        <div class="voter-row">
            <input id="voter-name" name="voterName" type="text" maxlength="40" placeholder="e.g. Taylor" required>
            <button type="submit">Start Voting</button>
        </div>
        <p id="voter-message" role="status" aria-live="polite"></p>
    </form>

    <div id="voting-app" hidden>
        <div class="status-panel" aria-live="polite">
            <p id="active-user"></p>
            <p id="remaining-votes"></p>
        </div>
        <ul id="proposal-list"></ul>
    </div>
</section>

<style>
    #dot-democracy {
        margin-top: 1.5rem;
        padding: 1.25rem;
        border: 1px solid #d7e2eb;
        border-radius: 10px;
        background: #f8fbfe;
    }

    #voter-form {
        display: grid;
        gap: 0.5rem;
    }

    #voter-form label {
        font-size: 0.95rem;
        font-weight: 600;
    }

    .voter-row {
        display: grid;
        grid-template-columns: minmax(180px, 320px) auto;
        gap: 0.5rem;
        align-items: center;
    }

    #voter-name {
        border: 1px solid #c3cfda;
        border-radius: 6px;
        padding: 0.5rem 0.65rem;
        font-size: 1rem;
    }

    #voter-form button,
    .proposal-controls button {
        border: 0;
        border-radius: 6px;
        padding: 0.55rem 0.85rem;
        cursor: pointer;
        font-weight: 600;
    }

    #voter-message {
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

    @media (max-width: 680px) {
        .voter-row {
            grid-template-columns: 1fr;
        }

        #voter-form button {
            width: 100%;
        }

        .proposal-card {
            grid-template-columns: 1fr;
            align-items: start;
        }

        .proposal-controls {
            justify-content: start;
        }
    }
</style>

<script>
    (() => {
        const MAX_VOTES_PER_USER = 5;
        const STORAGE_KEY = 'dot-democracy-mvp-v1';
        const proposals = [
            { id: 'support-hours', title: 'Extend support hours' },
            { id: 'feature-requests', title: 'Public feature request board' },
            { id: 'docs-refresh', title: 'Refresh site documentation' },
            { id: 'mobile-layout', title: 'Improve mobile layout' },
            { id: 'community-events', title: 'Run monthly community events' }
        ];

        const voterForm = document.getElementById('voter-form');
        const voterNameInput = document.getElementById('voter-name');
        const voterMessage = document.getElementById('voter-message');
        const votingApp = document.getElementById('voting-app');
        const activeUser = document.getElementById('active-user');
        const remainingVotes = document.getElementById('remaining-votes');
        const proposalList = document.getElementById('proposal-list');

        const sanitizeName = (name) => name.trim().toLowerCase();
        const displayName = (name) => name.trim();

        const defaultState = {
            users: {}
        };

        const getState = () => {
            try {
                const raw = localStorage.getItem(STORAGE_KEY);
                if (!raw) {
                    return structuredClone(defaultState);
                }

                const parsed = JSON.parse(raw);
                return parsed && parsed.users ? parsed : structuredClone(defaultState);
            } catch {
                return structuredClone(defaultState);
            }
        };

        const saveState = (state) => {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        };

        const ensureUserVotes = (state, userKey) => {
            if (!state.users[userKey]) {
                state.users[userKey] = {};
            }

            proposals.forEach((proposal) => {
                if (!Number.isInteger(state.users[userKey][proposal.id])) {
                    state.users[userKey][proposal.id] = 0;
                }
            });
        };

        const totalVotesByUser = (state, userKey) => {
            ensureUserVotes(state, userKey);
            return proposals.reduce((sum, proposal) => sum + state.users[userKey][proposal.id], 0);
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
                voterMessage.textContent = `You have already used all ${MAX_VOTES_PER_USER} votes.`;
                return;
            }

            if (delta < 0 && currentValue <= 0) {
                return;
            }

            state.users[currentUserKey][proposalId] = currentValue + delta;
            saveState(state);
            voterMessage.textContent = '';
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
            proposals.forEach((proposal) => {
                proposalList.appendChild(proposalCard(state, proposal));
            });
        };

        voterForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const entered = displayName(voterNameInput.value);
            const userKey = sanitizeName(entered);

            if (!userKey) {
                voterMessage.textContent = 'Enter your name to begin voting.';
                return;
            }

            const state = getState();
            ensureUserVotes(state, userKey);
            saveState(state);

            currentUserKey = userKey;
            currentUserLabel = entered;
            votingApp.hidden = false;
            voterMessage.textContent = '';
            render(state);
        });
    })();
</script>
