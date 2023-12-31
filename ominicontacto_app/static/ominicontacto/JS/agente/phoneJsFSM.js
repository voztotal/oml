/* Copyright (C) 2018 Freetech Solutions

 This file is part of OMniLeads

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License version 3, as published by
 the Free Software Foundation.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see http://www.gnu.org/licenses/.

*/

/* Requirements:                        */
/*      - state-machine-min.js          */

/* global StateMachine */

var PhoneFSM = new StateMachine.factory({
    init: 'Inactive',
    transitions: [
        // Inactive
        { name: 'start',                  from: 'Inactive',           to: 'Initial' },
        // Initial
        { name: 'registered',             from: 'Initial',            to: 'LoggingToAsterisk' },
        { name: 'disconnected',           from: 'Initial',            to: 'End' },
        { name: 'failedRegistration',     from: 'Initial',            to: 'End' },

        // LoggingToAsterisk
        { name: 'logToAsteriskOk',        from: 'LoggingToAsterisk',  to: 'Ready' },
        { name: 'logToAsteriskError',     from: 'LoggingToAsterisk',  to: 'End' },

        // Ready
        { name: 'receiveCall',            from: 'Ready',              to: 'ReceivingCall' },
        { name: 'startPause',             from: 'Ready',              to: 'Pausing' },
        { name: 'logout',                 from: 'Ready',              to: 'End' },
        { name: 'unregistered',           from: 'Ready',              to: 'ConnLossReady' },
        { name: 'failedRegistration',     from: 'Ready',              to: 'ConnLossReady' },
        // ConnLossReady
        { name: 'unregistered',           from: 'ConnLossReady',      to: 'ConnLossReady' },
        { name: 'registered',             from: 'ConnLossReady',      to: 'Ready' },
        
        // Pausing
        { name: 'pauseSet',               from: 'Pausing',            to: 'Paused' },
        { name: 'pauseAborted',           from: 'Pausing',            to: 'Ready' },

        // Paused
        { name: 'unpause',                from: 'Paused',             to: 'Ready' },
        { name: 'receiveCall',            from: 'Paused',             to: 'ReceivingCall' },
        { name: 'logout',                 from: 'Paused',             to: 'End' },
        { name: 'changePause',            from: 'Paused',             to: 'Pausing' },
        { name: 'unregistered',           from: 'Paused',             to: 'ConnLossPaused' },
        { name: 'failedRegistration',     from: 'Paused',             to: 'ConnLossPaused' },
        // ConnLossPaused
        { name: 'unregistered',           from: 'ConnLossPaused',     to: 'ConnLossPaused' },
        { name: 'registered',             from: 'ConnLossPaused',     to: 'Paused' },

        // OnCall
        { name: 'endCall',                from: 'OnCall',             to: 'Ready' },
        { name: 'dialTransfer',           from: 'OnCall',             to: 'DialingTransfer' },
        { name: 'startOnHold',            from: 'OnCall',             to: 'OnHold' },
        // DialingTransfer
        { name: 'endCall',                from: 'DialingTransfer',    to: 'Ready' },
        { name: 'blindTransfer',          from: 'DialingTransfer',    to: 'Transfered' },
        { name: 'consultativeTransfer',   from: 'DialingTransfer',    to: 'Transfering' },
        // Transfered
        { name: 'endCall',                from: 'Transfered',         to: 'Ready' },
        // Transfering
        { name: 'transferAccepted',       from: 'Transfering',        to: 'Ready' },
        { name: 'endCall',                from: 'Transfering',        to: 'Ready' },
        { name: 'transferNotAccepted',    from: 'Transfering',        to: 'OnCall' }, // Cuando sucede?
        { name: 'endTransfer',            from: 'Transfering',        to: 'OnCall' },

        // ReceivingCall
        { name: 'acceptCall',             from: 'ReceivingCall',      to: 'OnCall' },
        { name: 'refuseCall',             from: 'ReceivingCall',      to: 'Ready' },
        // OnHold
        { name: 'releaseHold',            from: 'OnHold',             to: 'OnCall' },
        { name: 'endCall',                from: 'OnHold',             to: 'Ready' },


        /*/ DEPRECATED: All calls are started from Asterisk.
        // Calling
        { name: 'startCall',              from: 'Ready',              to: 'Calling' },
        { name: 'endCall',                from: 'Calling',            to: 'Ready' },
        { name: 'connectCall',            from: 'Calling',            to: 'OnCall' },
        { name: 'startCall',              from: 'Paused',             to: 'Calling' },
        /**/
    ],

});
